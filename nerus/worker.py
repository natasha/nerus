
from .const import (
    WORKER_ANNOTATOR,
    WORKER_QUEUE,

    CORPUS,
)
from .queue import (
    get_queue,
    work_on
)
from .db import (
    get_db,

    query_index,
    chunk_insert,

    doc_texts,
    as_bsons
)
from .annotators import find as find_annotator


def task(ids, annotator=WORKER_ANNOTATOR):
    db = get_db()
    docs = query_index(db[CORPUS], ids)

    texts = doc_texts(docs)
    constructor = find_annotator(annotator)
    annotator = constructor()
    markups = annotator(texts)

    docs = as_bsons(markups)
    chunk_insert(db[annotator.name], docs, 10)


def run(queue=WORKER_QUEUE, annotator=WORKER_ANNOTATOR):
    constructor = find_annotator(annotator)
    annotator = constructor()
    annotator.wait()

    queue = get_queue(queue)
    work_on(queue)
