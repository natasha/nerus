
from .utils import strict_zip
from .const import (
    WORKER_ANNOTATOR,
    WORKER_QUEUE,
    CORPUS,
    _ID, TEXT
)
from .queue import (
    get_queue,
    work_on
)
from .db import (
    get_db,

    query_index,
    chunk_insert,
)
from .annotators import find as find_annotator


def decode_corpus(docs):
    ids = []
    texts = []
    for doc in docs:
        ids.append(doc[_ID])
        texts.append(doc[TEXT])
    return ids, texts


def encode_markups(markups, ids):
    for markup, id in strict_zip(markups, ids):
        doc = markup.as_bson
        doc[_ID] = id
        yield doc


def task(ids, annotator=WORKER_ANNOTATOR):
    db = get_db()
    docs = query_index(db[CORPUS], ids)

    ids, texts = decode_corpus(docs)
    constructor = find_annotator(annotator)
    annotator = constructor()
    markups = list(annotator.map(texts))

    docs = encode_markups(markups, ids)
    chunk_insert(db[annotator.name], docs, 100)


def run(queue=WORKER_QUEUE, annotator=WORKER_ANNOTATOR):
    constructor = find_annotator(annotator)
    annotator = constructor()
    annotator.wait()

    queue = get_queue(queue)
    work_on(queue)
