
from nerus.utils import (
    head,
    group_chunks
)
from nerus.log import (
    log,
    log_progress
)
from nerus.const import (
    CORPUS,
    ANNOTATORS,
)
from nerus.queue import (
    get_connection,
    get_queue,
    enqueue,
    show as show_queues__
)
from nerus.worker import task
from nerus.db import (
    get_db,
    read_index
)
from nerus.const import WORKER_HOST


def enqueue_tasks(args):
    annotators = args.annotators or ANNOTATORS
    enqueue_tasks_(annotators, args.offset, args.count, args.chunk)


def enqueue_tasks_(annotators, offset, count, chunk):
    log(
        'Annotators: %s; offset: %d, count: %d, chunk: %d',
        ', '.join(annotators), offset, count or -1, chunk
    )

    db = get_db(host=WORKER_HOST)
    ids = read_index(db[CORPUS], offset)
    ids = log_progress(ids)

    ids = head(ids, count)
    chunks = group_chunks(ids, size=chunk)

    connection = get_connection(host=WORKER_HOST)
    queues = {
        _: get_queue(_, connection)
        for _ in annotators
    }
    for chunk in chunks:
        for annotator in annotators:
            queue = queues[annotator]
            enqueue(queue, task, chunk)


def show_queues(args):
    show_queues_()


def show_queues_():
    log('Showing queues')
    connection = get_connection(host=WORKER_HOST)
    show_queues__(connection)
