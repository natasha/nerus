
from nerus.utils import (
    head,
    iter_len,
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
    get_queue,
    enqueue
)
from nerus.worker import task
from nerus.db import (
    get_db,
    read_index
)


def enqueue_tasks(args):
    annotators = args.annotators or ANNOTATORS
    enqueue_tasks_(annotators, args.offset, args.count, args.chunk, args.dry_run)


def enqueue_tasks_(annotators, offset, count, chunk, dry_run=False):
    log(
        'Annotators: %s; offset: %d, count: %d, chunk: %d',
        ', '.join(annotators), offset, count or -1, chunk
    )

    db = get_db()
    ids = read_index(db[CORPUS], offset)
    ids = log_progress(ids)

    ids = head(ids, count)
    chunks = group_chunks(ids, size=chunk)

    if dry_run:
        log('Annotators: %s; chunks: %d', ', '.join(annotators), iter_len(chunks))
    else:
        queues = {
            _: get_queue(_)
            for _ in annotators
        }
        for chunk in chunks:
            for annotator in annotators:
                queue = queues[annotator]
                enqueue(queue, task, chunk)
