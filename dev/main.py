
from os.path import (
    exists, expanduser,
    join as join_path
)
from collections import defaultdict
from itertools import islice as head
import json
import gzip

import boto3
import requests

from tqdm.notebook import tqdm as log_progress

from corus import load_lenta
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

S3_LENTA = LENTA
S3_NER = NER
S3_MORPH = MORPH
S3_SYNTAX = SYNTAX

#######
#  PROCESS
######

HOST = 'localhost'
NER_PORT = 8080
MORPH_PORT = 8081
SYNTAX_PORT = 8082
CHUNK_SIZE = 10000
# ~5/100k > 128
SENT_LEN = 128

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


class Record(object):
    __attributes__ = []

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
#   PROCESS
#
#####


def process_call(data, host, port):
    url = f'http://{host}:{port}'
    response = requests.post(
        url,
        json=data
    )
    response.raise_for_status()
    return response.json()


#######
#   NER
#######


def ner_chunks(records, chunk_size):
    chunks = chop(records, chunk_size)
    for chunk in chunks:
        yield [_.text for _ in chunk]


def process_ner(records, host=HOST, port=NER_PORT, chunk_size=CHUNK_SIZE):
    for chunk in ner_chunks(records, chunk_size):
        data = process_call(chunk, host, port)
        yield from data


#########
#  MORPH
########


def morph_items(records, sent_len):
    for record in records:
        sents = sentenize(record.text)
        for sent in sents:
            tokens = tokenize(sent.text)
            tokens = head(tokens, sent_len)
            yield [_.text for _ in tokens]


def morph_chunks(records, chunk_size, sent_len):
    items = morph_items(records, sent_len)
    yield from chop(items, chunk_size)


def process_morph(records, host=HOST, port=MORPH_PORT,
                  chunk_size=CHUNK_SIZE, sent_len=SENT_LEN):
    for chunk in morph_chunks(records, chunk_size, sent_len):
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
        data = process_call(group, host, port)
        yield from data


def process_syntax(records, host=HOST, port=SYNTAX_PORT,
                   chunk_size=CHUNK_SIZE, sent_len=SENT_LEN):
    for chunk in syntax_chunks(records, chunk_size, sent_len):
        order, groups = order_size(chunk)
        data = process_size(groups, host, port)
        yield from reorder(data, order)

