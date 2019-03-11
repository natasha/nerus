
from .utils import group_chunks
from .db import (
    read_index,
    query_index,
)
from .const import (
    _ID,
    TEXT
)
from .etl import (
    serialize_jsonl,
    dump_gz_lines,
    append_tar
)
from .path import maybe_rm


JSONL_GZ = '.jsonl.gz'


def read_collection(collection, count, chunk):
    ids = read_index(collection, count=count)
    chunks = group_chunks(ids, size=chunk)
    for chunk in chunks:
        docs = query_index(collection, ids=chunk, include_missing=True)
        for doc in docs:
            yield doc


def encode_corpus(docs):
    for doc in docs:
        doc.pop(_ID)
        yield doc


def encode_annotator(docs):
    for doc in docs:
        if doc:  # in case annotator failed on text
            doc.pop(_ID)
            doc.pop(TEXT)
        yield doc


def dump_collection(path, name, docs):
    lines = serialize_jsonl(docs)
    part = name + JSONL_GZ
    try:
        dump_gz_lines(lines, part)
        append_tar(path, part)
    except:
        maybe_rm(path)
        raise
    finally:
        maybe_rm(part)
