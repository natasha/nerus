
from .utils import (
    Record,
    group_chunks,
)
from .db import (
    read_index,
    query_index,
)
from .etl import (
    load_gz_lines,
    parse_jsonl
)
from .const import SOURCE
from .annotators import AnnotatorMarkup
from .sources import SourceRecord


class DumpRecord(Record):
    __attributes__ = ['source', 'markups']
    __annotations__ = {
        'source': SourceRecord,
        'markups': [AnnotatorMarkup]
    }

    def __init__(self, source, markups):
        self.source = source
        self.markups = markups


def query_index_(db, collection, chunk, Record):
    docs = query_index(db[collection], ids=chunk, include_missing=True)
    return (Record.from_bson(_) for _ in docs)


def query_indexes(db, collections, chunk, Record):
    for collection in collections:
        yield query_index_(db, collection, chunk, Record)


def dump(db, annotators, count, chunk):
    ids = read_index(db[SOURCE], count=count)
    chunks = group_chunks(ids, size=chunk)
    for chunk in chunks:
        source = query_index_(db, SOURCE, chunk, SourceRecord)
        markups = query_indexes(db, annotators, chunk, AnnotatorMarkup)
        for source, *markups in zip(source, *markups):
            yield DumpRecord(source, markups)


def load(path):
    lines = load_gz_lines(path)
    records = parse_jsonl(lines)
    for record in records:
        yield DumpRecord.from_json(record)
