
from os.path import (
    exists, expanduser,
    join as join_path
)
from collections import defaultdict, OrderedDict
from itertools import (
    islice as head,
    groupby,
)
import json
import gzip

import boto3
import requests

from tqdm.notebook import tqdm as log_progress

from corus import load_lenta as load_lenta_
from razdel import sentenize, tokenize


#####
#
#  CONST
#
#####

######
#  PATH
#######

DATA_DIR = 'data'

LENTA = join_path(DATA_DIR, 'lenta-ru-news.csv.gz')
LENTA_TOTAL = 739351

NER = join_path(DATA_DIR, 'ner.jl.gz')
MORPH = join_path(DATA_DIR, 'morph.jl.gz')
SYNTAX = join_path(DATA_DIR, 'syntax.jl.gz')
NERUS = join_path(DATA_DIR, 'nerus_lenta.conllu.gz')

S3_LENTA = LENTA
S3_NER = NER
S3_MORPH = MORPH
S3_SYNTAX = SYNTAX
S3_NERUS = NERUS

#######
#  PROCESS
######

HOST = 'localhost'
NER_PORT = 8080
MORPH_PORT = 8081
SYNTAX_PORT = 8082
NER_CHUNK_SIZE = 10000
MORPH_CHUNK_SIZE = 100000
SYNTAX_CHUNK_SIZE = 1000000

#####
#  BIO
#######

B = 'B'
I = 'I'
O = 'O'

######
#  CONFIG
#####


def load_json(path, encoding='utf8'):
    with open(path, encoding=encoding) as file:
        return json.load(file)


config = {}
path = expanduser('~/.nerus.json')
if exists(path):
    config = load_json(path)

########
#  S3
######

S3_KEY_ID = config.get('s3_key_id')
S3_KEY = config.get('s3_key')
S3_BUCKET = 'natasha-nerus'
S3_REGION = 'us-east-1'
S3_ENDPOINT = 'https://storage.yandexcloud.net'


########
#
#  IO
#
#####


def load_gz_lines(path, encoding='utf8'):
    with gzip.open(path) as file:
        for line in file:
            yield line.decode(encoding).rstrip()


def dump_gz_lines(lines, path):
    with gzip.open(path, 'wt') as file:
        for line in lines:
            file.write(line + '\n')


def format_jl(items):
    for item in items:
        yield json.dumps(item, ensure_ascii=False)


def parse_jl(lines):
    for line in lines:
        yield json.loads(line)


#######
#
#   RECORD
#
#######


def parse_annotation(annotation):
    type = annotation or str

    repeatable = False
    if isinstance(annotation, list):  # [Fact]
        repeatable = True
        type = annotation[0]

    is_record = issubclass(type, Record)

    return type, repeatable, is_record


class Record(object):
    __attributes__ = []
    __annotations__ = {}

    def __init__(self, *args, **kwargs):
        for key, value in zip(self.__attributes__, args):
            self.__dict__[key] = value
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and all(
                (getattr(self, _) == getattr(other, _))
                for _ in self.__attributes__
            )
        )

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return (getattr(self, _) for _ in self.__attributes__)

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        name = self.__class__.__name__
        args = ', '.join(
            '{key}={value!r}'.format(
                key=_,
                value=getattr(self, _)
            )
            for _ in self.__attributes__
        )
        return '{name}({args})'.format(
            name=name,
            args=args
        )

    def _repr_pretty_(self, printer, cycle):
        name = self.__class__.__name__
        if cycle:
            printer.text('{name}(...)'.format(name=name))
        else:
            printer.text('{name}('.format(name=name))
            keys = self.__attributes__
            size = len(keys)
            if size:
                with printer.indent(4):
                    printer.break_()
                    for index, key in enumerate(keys):
                        printer.text(key + '=')
                        value = getattr(self, key)
                        printer.pretty(value)
                        if index < size - 1:
                            printer.text(',')
                            printer.break_()
                printer.break_()
            printer.text(')')

    @property
    def as_json(self):
        data = OrderedDict()
        for key in self.__attributes__:
            annotation = self.__annotations__.get(key)
            _, repeatable, is_record = parse_annotation(annotation)

            value = getattr(self, key)
            if value is None:
                continue

            if repeatable and is_record:
                value = [_.as_json for _ in value]
            elif is_record:
                value = value.as_json

            data[key] = value
        return data

    @classmethod
    def from_json(cls, data):
        args = []
        for key in cls.__attributes__:
            annotation = cls.__annotations__.get(key)
            type, repeatable, is_record = parse_annotation(annotation)
            value = data.get(key)
            if value is None and repeatable:
                value = []
            elif value is not None:
                if repeatable and is_record:
                    value = [type.from_json(_) for _ in value]
                elif is_record:
                    value = type.from_json(value)
            args.append(value)
        return cls(*args)


########
#
#   S3
#
#######


class S3(Record):
    __attributes__ = ['key_id', 'key', 'bucket', 'endpoint', 'region']

    def __init__(self, key_id=S3_KEY_ID, key=S3_KEY, bucket=S3_BUCKET,
                 endpoint=S3_ENDPOINT, region=S3_REGION):
        self.key_id = key_id
        self.key = key
        self.bucket = bucket
        self.endpoint = endpoint
        self.region = region

        self.client = boto3.client(
            's3',
            aws_access_key_id=key_id,
            aws_secret_access_key=key,
            region_name=region,
            endpoint_url=endpoint,
        )

    def upload(self, path, key):
        self.client.upload_file(path, self.bucket, key)

    def download(self, key, path):
        self.client.download_file(self.bucket, key, path)


######
#
#  CHOP
#
#######


def chop(items, size):
    buffer = []
    for item in items:
        buffer.append(item)
        if len(buffer) >= size:
            yield buffer
            buffer = []
    if buffer:
        yield buffer


######
#
#  LENTA
#
#####


def load_lenta(path):
    for record in load_lenta_(path):
        if not record.text.strip():
            # ~5 texts / whole lenta
            continue
        yield record


######
#
#   PROCESS
#
#####


class ProcessError(Exception):
    pass


def process_call(data, host, port):
    url = f'http://{host}:{port}'
    response = requests.post(
        url,
        json=data
    )
    try:
        response.raise_for_status()
    except:
        raise ProcessError
    return response.json()


#######
#   NER
#######


def ner_chunks(records, chunk_size):
    chunks = chop(records, chunk_size)
    for chunk in chunks:
        yield [_.text for _ in chunk]


def process_ner(records, host=HOST, port=NER_PORT, chunk_size=NER_CHUNK_SIZE):
    for chunk in ner_chunks(records, chunk_size):
        data = process_call(chunk, host, port)
        yield from data


#########
#  MORPH
########


def morph_items(records):
    for record in records:
        sents = sentenize(record.text)
        for sent in sents:
            tokens = tokenize(sent.text)
            yield [_.text for _ in tokens]


def morph_chunks(records, chunk_size):
    items = morph_items(records)
    yield from chop(items, chunk_size)


def process_morph(records, host=HOST, port=MORPH_PORT, chunk_size=MORPH_CHUNK_SIZE):
    for chunk in morph_chunks(records, chunk_size):
        data = process_call(chunk, host, port)
        yield from data


#######
#   SYNTAX
########


syntax_chunks = morph_chunks


def order_size(chunk):
    sizes = defaultdict(list)
    for index, words in enumerate(chunk):
        sizes[len(words)].append([index, words])

    order = []
    groups = []
    for size in sorted(sizes):
        group = []
        for index, words in sizes[size]:
            order.append(index)
            group.append(words)
        groups.append(group)
    return order, groups


def reorder(items, order):
    reorder = [None] * len(order)
    for index, item in enumerate(items):
        reorder[order[index]] = item
    return reorder


def process_size(groups, host, port):
    for group in groups:
        try:
            data = process_call(group, host, port)
        except ProcessError:
            # rare cases of groups of too long sents (~0.007% 172/2496485)
            # concat trimed masks
            for _ in group:
                yield {}
        else:
            yield from data


def process_syntax(records, host=HOST, port=SYNTAX_PORT, chunk_size=SYNTAX_CHUNK_SIZE):
    for chunk in syntax_chunks(records, chunk_size):
        order, groups = order_size(chunk)
        data = process_size(groups, host, port)
        yield from reorder(data, order)


#######
#
#   SPAN
#
#######


class Span(Record):
    __attributes__ = ['start', 'stop', 'type']

    def __init__(self, start, stop, type=None):
        self.start = start
        self.stop = stop
        self.type = type

    def offset(self, delta):
        return Span(
            self.start + delta,
            self.stop + delta,
            self.type
        )


def offset_spans(spans, delta):
    for span in spans:
        yield span.offset(delta)


def envelop_span(envelope, span):
    return envelope.start <= span.start and span.stop <= envelope.stop


def envelop_spans(envelope, spans):
    for span in spans:
        if envelop_span(envelope, span):
            yield span


########
#
#   MARKUP
#
##########


class NERMarkup(Record):
    __attributes__ = ['text', 'spans']
    __annotations__ = {
        'spans': [Span]
    }


class MorphToken(Record):
    __attributes__ = ['text', 'pos', 'feats']


class MorphMarkup(Record):
    __attributes__ = ['tokens']
    __annotations__ = {
        'tokens': [MorphToken]
    }


class SyntaxToken(Record):
    __attributes__ = ['id', 'text', 'head_id', 'rel']


class SyntaxMarkup(Record):
    __attributes__ = ['tokens']
    __annotations__ = {
        'tokens': [SyntaxToken]
    }


parse_ner_markup = NERMarkup.from_json
parse_morph_markup = MorphMarkup.from_json
parse_syntax_markup = SyntaxMarkup.from_json


#######
#
#   BIO
#
######


def format_bio(part, type):
    if not type:
        return part
    return '%s-%s' % (part, type)


def append_ellipsis(items, ellipsis=None):
    for item in items:
        yield item
    yield ellipsis


def spans_bio(tokens, spans):
    spans = append_ellipsis(spans)
    span = next(spans)
    for token in tokens:
        part = O
        type = None
        if span:
            if token.start >= span.start:
                type = span.type
                if token.start == span.start:
                    part = B
                else:
                    part = I
            if token.stop >= span.stop:
                span = next(spans)
        yield format_bio(part, type)


#######
#
#   TOKEN
#
########


class Token(Record):
    __attributes__ = ['start', 'stop', 'text']


def find_tokens(text, chunks):
    offset = 0
    for chunk in chunks:
        start = text.find(chunk, offset)
        stop = start + len(chunk)
        yield Token(start, stop, chunk)
        offset = stop


########
#
#   MERGE
#
#######


class MergeToken(Record):
    __attributes__ = ['id', 'text', 'pos', 'feats', 'head_id', 'rel', 'tag']


class MergeRecord(Record):
    __attributes__ = ['doc_id', 'sent_index', 'text', 'spans', 'tokens']


def sent_spans(sent, spans):
    spans = envelop_spans(sent, spans)
    return offset_spans(spans, -sent.start)    


def markup_words(markup):
    for token in markup.tokens:
        yield token.text


def merge_tokens(morphs, syntaxes, tags):
    for morph, syntax, tag in zip(morphs, syntaxes, tags):
        yield MergeToken(
            syntax.id, morph.text,
            morph.pos, morph.feats,
            syntax.head_id, syntax.rel,
            tag
        )


def merge(docs, ners, morphs, syntaxes):
    for doc_id, doc in enumerate(docs):
        ner = next(ners)
        sents = sentenize(doc.text)
        for sent_index, sent in enumerate(sents):
            morph = next(morphs)
            syntax = next(syntaxes)

            if len(morph.tokens) != len(syntax.tokens):
                # long sents
                # empty sent
                # syntax mask missaligned
                # ~250 sents / 100 000 texts
                continue

            spans = list(sent_spans(sent, ner.spans))
            words = markup_words(morph)
            tokens = find_tokens(sent.text, words)
            tags = spans_bio(tokens, spans)

            tokens = list(merge_tokens(morph.tokens, syntax.tokens, tags))
            yield MergeRecord(
                doc_id, sent_index,
                sent.text, spans, tokens
            )


######
#
#   CONLL
#
######


def format_feats(feats):
    if not feats:
        return '_'

    return '|'.join(
        '%s=%s' % (_, feats[_])
        for _ in sorted(feats)
    )


def format_merge_conll(records):
    # https://universaldependencies.org/format.html

    # ID, FORM, LEMMA,
    # UPOS, XPOS, FEATS
    # HEAD, DEPREL, DEPS
    # MISC    

    # # newdoc id = mf920901-001
    # # newpar id = mf920901-001-p1
    # # sent_id = mf920901-001-p1s1A
    # # text = Slovenská ústava: pro i proti
    # # text_en = Slovak constitution: pros and cons
    # 1   Slovenská   slovenský   ADJ     AAFS1----1A---- Case=Nom|Degree=Pos|...
    # 2   ústava      ústava      NOUN    NNFS1-----A---- Case=Nom|Gender=Fem|...
    # 3   :           :           PUNCT   Z:------------- _          2       p...
    # 4   pro         pro         ADP     RR--4---------- Case=Acc   2       a...

    for doc_id, group in groupby(records, key=lambda _: _.doc_id):
        yield f'# newdoc id = {doc_id}'
        for record in group:
            sent_id = f'{record.doc_id}_{record.sent_index}'
            yield f'# sent_id = {sent_id}'
            yield f'# text = {record.text}'
            for token in record.tokens:
                feats = format_feats(token.feats)
                yield (
                    f'{token.id}\t{token.text}\t_'  # no lemma
                    f'\t{token.pos}\t_\t{feats}'  # just pos, no xpos
                    f'\t{token.head_id}\t{token.rel}\t_'  # just deprel, no deps
                    f'\tTag={token.tag}'  # misc = ner tag
                )
            yield ''
