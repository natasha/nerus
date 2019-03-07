
from pymongo import MongoClient

from .const import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USERNAME,
    DB_PASSWORD,

    _ID
)


def get_db(host=DB_HOST, port=DB_PORT):
    client = MongoClient(
        host, port,
        username=DB_USERNAME,
        password=DB_PASSWORD
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


def query_index(collection, ids):
    return collection.find({_ID: {'$in': list(ids)}})


def read_index(collection, offset=0, count=None):
    if not count:
        count = 0  # no limit
    docs = collection.find({}).skip(offset).limit(count)
    for doc in docs:
        yield doc[_ID]


def get_stats(db):
    for name in db.list_collection_names():
        count = db[name].estimated_document_count()
        yield count, name
