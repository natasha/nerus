
from collections import defaultdict

from nerus.utils import (
    head,
    group_chunks
)
from nerus.log import (
    log,
    log_progress
)
from nerus.const import (
    SOURCE,
    ANNOTATORS,
    FAILED
)
from nerus.queue import (
    get_connection,
    get_queue,
    get_queues,
    enqueue,
    show
)
from nerus.worker import task
from nerus.db import (
    get_db,
    read_index
)
from nerus.const import WORKER_HOST


def queue_insert(args):
    annotators = args.annotators or ANNOTATORS
    queue_insert_(annotators, args.offset, args.count, args.chunk)


def queue_insert_(annotators, offset, count, chunk):
    log(
        'Annotators: %s; offset: %d, count: %d, chunk: %d',
        ', '.join(annotators), offset, count or -1, chunk
    )

    db = get_db(host=WORKER_HOST)
    ids = read_index(db[SOURCE], offset)
    ids = log_progress(ids, total=count)

    ids = head(ids, count)
    chunks = group_chunks(ids, size=chunk)

    connection = get_connection(host=WORKER_HOST)
    queues = dict(get_queues(annotators, connection))
    for chunk in chunks:
        for annotator in annotators:
            queue = queues[annotator]
            enqueue(queue, task, chunk)


def queue_show(args):
    queue_show_()


def queue_show_():
    log('Showing queues')
    connection = get_connection(host=WORKER_HOST)
    show(connection)


def queue_failed(args):
    queue_failed_()


def queue_failed_():
    log('Listing failed')
    connection = get_connection(host=WORKER_HOST)
    queue = get_queue(FAILED, connection=connection)
    for job in queue.jobs:
        print('Origin: %s' % job.origin)
        print('Id: %s' % job.get_id())
        print(job.exc_info, end='\n\n')


def queue_retry(args):
    queue_retry_(args.chunk)


def annotators_ids(jobs):
    ids = defaultdict(list)
    for job in jobs:
        annotator_ids, = job.args
        ids[job.origin].extend(annotator_ids)
    return ids


def queue_retry_(chunk):
    log('Retrying')
    connection = get_connection(host=WORKER_HOST)
    queue = get_queue(FAILED, connection=connection)

    ids = annotators_ids(queue.jobs)
    queue.empty()

    for annotator in ids:
        annotator_ids = ids[annotator]
        annotator_ids = log_progress(annotator_ids, prefix=annotator)
        chunks = group_chunks(annotator_ids, size=chunk)
        queue = get_queue(annotator, connection=connection)
        for chunk_ in chunks:
            enqueue(queue, task, chunk_)
