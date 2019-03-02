
from pymongo import MongoClient
from bson import ObjectId
from hashlib import md5
from time import sleep
from concurrent.futures import ThreadPoolExecutor

from .const import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USERNAME,
    DB_PASSWORD,

    DEEPPAVLOV,
    MITIE,
    NATASHA,
    PULLENTI,
    TEXTERRA,
    TOMITA,

    WORKER_ANNS
)
from .log import log
from .anns import (
    deeppavlov,
    mitie,
    natasha,
    pullenti,
    texterra,
    tomita
)


ANNS = {
    DEEPPAVLOV: deeppavlov,
    MITIE: mitie,
    NATASHA: natasha,
    PULLENTI: pullenti,
    TEXTERRA: texterra,
    TOMITA: tomita
}


#########
#
#   DB
#
##########


TEXT = 'text'
_ID = '_id'
CORPUS = 'corpus'


def get_db(host=DB_HOST, port=DB_PORT):
    client = MongoClient(
        host, port,
        username=DB_USERNAME,
        password=DB_PASSWORD
    )
    return client[DB_NAME]


##########
#
#   INSERT
#
########


def text_hash(text):
    bytes = text.encode('utf8')
    return md5(bytes).hexdigest()


def hash_id(hash):
    # https://docs.mongodb.com/manual/reference/method/ObjectId/
    return ObjectId(hash[:24])


def uniq(docs):
    cache = set()
    for doc in docs:
        id = doc[_ID]
        if id not in cache:
            yield doc
        cache.add(id)


class Buffer:
    def __init__(self, collection, size):
        self.collection = collection
        self.size = size

        self.docs = []
        self.append = self.docs.append


class InsertBuffer(Buffer):
    def maybe_flush(self):
        if len(self.docs) >= self.size:
            self.flush()

    def flush(self):
        if self.docs:
            self.insert()
            self.docs.clear()

    def insert(self):
        # find docs that are already in db
        ids = [_[_ID] for _ in self.docs]
        matches = self.collection.find({_ID: {'$in': ids}}, {_ID: 1})
        indb = {_[_ID] for _ in matches}

        # just in case same docs in current buffer
        docs = uniq(self.docs)

        # docs to insert
        docs = [_ for _ in docs if _[_ID] not in indb]
        if docs:
            self.collection.insert_many(docs)

    def extend(self, docs):
        for doc in docs:
            self.append(doc)
            self.maybe_flush()
        self.flush()


############
#
#   CORPUS
#
#########


def encode_corpus(records):
    for record in records:
        doc = record.as_json
        hash = text_hash(record.text)
        doc[_ID] = hash_id(hash)
        yield doc


def insert_corpus(db, records):
    docs = encode_corpus(records)
    buffer = InsertBuffer(db[CORPUS], 1000)
    buffer.extend(docs)


def load_corpus(db):
    return db[CORPUS].find({})


def corpus_texts(docs):
    for doc in docs:
        yield doc[TEXT]


#######
#
#   MARKUP
#
########


class DoneBuffer(Buffer):
    def maybe_flush(self):
        if len(self.docs) >= self.size:
            yield from self.flush()

    def flush(self):
        if self.docs:
            yield from self.update()
            self.docs.clear()

    def update(self):
        ids = [_[_ID] for _ in self.docs]
        matches = self.collection.find({_ID: {'$in': ids}}, {_ID: 1})
        indb = {_[_ID] for _ in matches}

        for doc in self.docs:
            if doc[_ID] not in indb:
                yield doc

    def filter(self, docs):
        for doc in docs:
            self.append(doc)
            yield from self.maybe_flush()
        yield from self.flush()


def encode_markups(records):
    for record in records:
        doc = record.as_json
        hash = text_hash(record.text)
        id = hash_id(hash)
        doc[TEXT] = id
        doc[_ID] = id
        yield doc


def run_loop(db, name, ann):
    log('Start loop: %s', name)
    done = DoneBuffer(db[name], 1000)

    corpus = load_corpus(db)
    todo = done.filter(corpus)

    texts = corpus_texts(todo)
    markups = ann.call(texts)

    docs = encode_markups(markups)
    buffer = InsertBuffer(db[name], 10)
    buffer.extend(docs)
    log('Stop loop: %s', name)


def run_ann(db, name, ann, timeout=10):
    log('Starting %s', name)
    try:
        ann.warmup()
    except:
        log('Failed to start %s', name)
        return
    else:
        log('Started %s', name)

    while True:
        run_loop(db, name, ann)
        sleep(timeout)


def get_pool():
    size = len(WORKER_ANNS)
    return ThreadPoolExecutor(max_workers=size)


def run(db):
    with get_pool() as pool:
        for name in WORKER_ANNS:
            ann = ANNS[name]
            pool.submit(run_ann, db, name, ann)
