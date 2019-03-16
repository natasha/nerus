
from .utils import strict_zip
from .const import (
    WORKER_ANNOTATOR,
    WORKER_QUEUE,
    SOURCE,
    _ID, TEXT
)
from .queue import (
    get_connection,
    get_queue,
    work_on
)
from .db import (
    get_db,
    query_index,
    chunk_insert,
)
from .annotators import Annotator
from .const import (
    YC_HDD,
    YC_UBUNTU_1604,
)


CONFIG = dict(
    cores=10,
    share=100,
    memory=20,
    disk_size=50,
    disk_type=YC_HDD,
    image=YC_UBUNTU_1604,
    spot=True,
)


def decode_source(docs):
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


def task(ids, annotator=WORKER_ANNOTATOR, chunk=100):
    db = get_db()
    docs = query_index(db[SOURCE], ids)

    ids, texts = decode_source(docs)
    constructor = Annotator.find(annotator)
    annotator = constructor()
    markups = list(annotator.map(texts))

    docs = encode_markups(markups, ids)
    chunk_insert(db[annotator.name], docs, chunk)


def run(queue=WORKER_QUEUE, annotator=WORKER_ANNOTATOR):
    constructor = Annotator.find(annotator)
    annotator = constructor()
    annotator.wait()

    connection = get_connection()
    queue = get_queue(queue, connection)
    work_on(queue)
