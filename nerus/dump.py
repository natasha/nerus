
from collections import OrderedDict

from .utils import group_chunks
from .db import (
    read_index,
    query_index,
)
from .etl import (
    load_gz_lines,
    parse_jsonl,
    serialize_jsonl,
    dump_gz_lines
)
from .const import (
    SOURCE,
    DEEPPAVLOV, TEXTERRA, PULLENTI, TOMITA
)
from .annotators import AnnotatorMarkup
from .sources import SourceRecord
from .span import Span
from .markup import (
    Markup,
    Multimarkup
)


###########
#
#   RAW
#
##########


class DumpRecord(Multimarkup):
    __attributes__ = ['source', 'markups']
    __annotations__ = {
        'source': SourceRecord,
        'markups': [AnnotatorMarkup]
    }

    def __init__(self, source, markups):
        self.source = source
        self.markups = markups

    @property
    def text(self):
        return self.source.text

    @property
    def sents(self):
        source = self.source.sents
        markups = (_.sents for _ in self.markups)
        for source, *markups in zip(source, *markups):
            yield DumpRecord(source, markups)

    def select(self, labels):
        return DumpRecord(
            self.source,
            [_ for _ in self.markups if _.label in labels]
        )

    def find(self, label):
        for markup in self.markups:
            if markup.label == label:
                return markup
        raise KeyError(label)


def query_index_(db, collection, chunk, Record):
    docs = query_index(db[collection], ids=chunk, include_missing=True)
    for doc in docs:
        if doc:
            yield Record.from_bson(doc)
        else:
            # include missing
            yield


def query_indexes(db, collections, chunk, Record):
    for collection in collections:
        yield query_index_(db, collection, chunk, Record)


def read_raw(db, annotators, count, chunk):
    ids = read_index(db[SOURCE], count=count)
    chunks = group_chunks(ids, size=chunk)
    for chunk in chunks:
        source = query_index_(db, SOURCE, chunk, SourceRecord)
        markups = query_indexes(db, annotators, chunk, AnnotatorMarkup)
        for source, *markups in zip(source, *markups):
            markups = filter(None, markups)  # since include_missing
            yield DumpRecord(source, list(markups))


def dump_raw(records, path):
    lines = serialize_jsonl(_.as_json for _ in records)
    dump_gz_lines(lines, path)


def load_raw(path):
    lines = load_gz_lines(path)
    records = parse_jsonl(lines)
    for record in records:
        yield DumpRecord.from_json(record)


##########
#
#    NORM
#
############


MIX = [DEEPPAVLOV, TEXTERRA, PULLENTI, TOMITA]


def norm_raw(records):
    for record in records:
        record = record.select(MIX)
        yield record.adapted.mixed


# {
#   "article_id": 100,
#   "content": " ... ",
#   "annotations": [
#       {
#         "span": {
#           "start": 10,
#           "end": 31
#         },
#         "type": "PER",
#         "text": "Дмитрием Светозаровым"
#       }
#   ]
# }


def serialize_spans(text, records):
    records = sorted(records, key=lambda _: _.start)
    for start, stop, type in records:
        chunk = text[start:stop]
        yield OrderedDict([
            ('span', OrderedDict([
                ('start', start),
                ('end', stop)
            ])),
            ('type', type),
            ('text', chunk)
        ])


def serialize_norm(records):
    for index, record in enumerate(records):
        spans = list(serialize_spans(record.text, record.spans))
        yield OrderedDict([
            ('article_id', index),
            ('content', record.text),
            ('annotations', spans)
        ])


def dump_norm(records, path):
    lines = serialize_jsonl(serialize_norm(records))
    dump_gz_lines(lines, path)


def parse_spans(items):
    for item in items:
        yield Span(
            item['span']['start'],
            item['span']['end'],
            item['type']
        )


def parse_norm(items):
    for item in items:
        yield Markup(
            item['content'],
            list(parse_spans(item['annotations']))
        )


def load_norm(path):
    lines = load_gz_lines(path)
    records = parse_jsonl(lines)
    return parse_norm(records)
