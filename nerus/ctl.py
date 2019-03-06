
import sys
import argparse

from .log import (
    log,
    log_progress
)
from .utils import (
    head,
    iter_len,
    group_chunks
)
from .const import (
    CORPUS,
    CORPORA,
    ANNOTATORS
)
from .corpora import find as find_corpus
from .db import (
    get_db,
    chunk_insert,
    read_index,
    diff_index
)
from .queue import (
    get_queue,
    enqueue
)
from .worker import (
    run as run_worker_,
    task
)


def insert_corpus(args):
    insert_corpus_(args.corpus)


def encode_corpus(corpus):
    for record in corpus:
        yield record.as_bson


def insert_corpus_(name):
    schema = find_corpus(name)
    path = schema.get()
    corpus = schema.load(path)

    db = get_db()
    docs = encode_corpus(corpus)
    log('Insert %s -> db.%s', name, CORPUS)
    chunk_insert(db[CORPUS], log_progress(docs), 1000)


def run_worker(args):
    log('Starting worker')
    run_worker_()


def enqueue_tasks(args):
    annotators = args.annotators
    if not annotators:
        annotators = ANNOTATORS
    for annotator in annotators:
        enqueue_tasks_(annotator, args.offset, args.count, args.chunk, args.dry_run)


def enqueue_tasks_(annotator, offset, count, chunk, dry_run=False):
    log(
        '%s <- offset: %d, count: %d, chunk: %d',
        annotator, offset, count or -1, chunk
    )

    db = get_db()
    ids = read_index(db[CORPUS], offset)
    ids = log_progress(ids, label='Corpus')

    ids = diff_index(db[annotator], ids)
    ids = log_progress(ids, label='Todo')

    ids = head(ids, count)
    chunks = group_chunks(ids, size=chunk)

    if dry_run:
        log('%s <- chunks planned: %d', annotator, iter_len(chunks))
    else:
        queue = get_queue(annotator)
        count = 0
        for chunk in chunks:
            enqueue(queue, task, chunk)
            count += 1
        log('%s <- chunks: %d', annotator, count)


def main():
    parser = argparse.ArgumentParser(prog='ctl')
    parser.set_defaults(function=None)

    subs = parser.add_subparsers()

    db = subs.add_parser('db').add_subparsers()

    sub = db.add_parser('insert')
    sub.set_defaults(function=insert_corpus)
    sub.add_argument('corpus', choices=CORPORA)

    sub = subs.add_parser('worker')
    sub.set_defaults(function=run_worker)

    sub = subs.add_parser('q')
    sub.set_defaults(function=enqueue_tasks)
    sub.add_argument('annotators', nargs='*', choices=ANNOTATORS)
    sub.add_argument('--offset', type=int, default=0)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=1000)
    sub.add_argument('--dry-run', action='store_true')

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if not args.function:
        parser.print_help()
        parser.exit()
    args.function(args)


if __name__ == '__main__':
    main()
