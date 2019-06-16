
from collections import OrderedDict

from .const import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USERNAME,
    DB_PASSWORD,

    _ID
)


def get_db(host=DB_HOST, port=DB_PORT):
    from pymongo import MongoClient

    client = MongoClient(
        host, port,
        username=DB_USERNAME,
        password=DB_PASSWORD,
        document_class=OrderedDict
    )
    return client[DB_NAME]


class Buffer:
    def __init__(self, collection, size):
        self.collection = collection
        self.size = size

        self.docs = []
        self.append = self.docs.append

    def maybe_flush(self):
        if len(self.docs) >= self.size:
            self.flush()

    def flush(self):
        if self.docs:
            self.collection.insert_many(self.docs)
            self.docs.clear()


def chunk_insert(collection, docs, size):
    buffer = Buffer(collection, size)
    for doc in docs:
        buffer.append(doc)
        buffer.maybe_flush()
    buffer.flush()


def query_index(collection, ids, include_missing=False):
    docs = collection.find({_ID: {'$in': list(ids)}})
    mapping = {_[_ID]: _ for _ in docs}
    for id in ids:
        if id in mapping:
            yield mapping[id]
        elif include_missing:
            yield


def read_index(collection, offset=0, count=None, chunk=1000):
    if not count:
        count = 0  # no limit
    docs = (
        collection
        .find({}, {_ID: 1})
        # https://stackoverflow.com/questions/32731140/how-to-get-rid-of-cursor-id-error-in-mongodb/34261202
        .batch_size(chunk)
        .sort(_ID, 1)
        .skip(offset)
        .limit(count)
    )
    for doc in docs:
        yield doc[_ID]
