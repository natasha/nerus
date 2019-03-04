
import sys
import argparse

from .log import (
    log,
    log_progress
)
from .utils import group_chunks
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
    as_bsons
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


def insert_corpus_(name):
    schema = find_corpus(name)
    path = schema.get()
    corpus = schema.load(path)

    db = get_db()
    docs = as_bsons(corpus)
    log('Insert %s -> db.%s', name, CORPUS)
    chunk_insert(db[CORPUS], log_progress(docs), 1000)


def run_worker(args):
    log('Starting worker')
    run_worker_()


def enqueue_tasks(args):
    enqueue_tasks_(args.annotator, args.offset, args.count, args.chunk)


def enqueue_tasks_(queue, offset, count, chunk):
    log('Enqueue %s <- corpus[%d:+%r:%d]' % (queue, offset, count, chunk))
    db = get_db()
    ids = read_index(db[CORPUS], offset, count)
    ids = log_progress(ids)
    chunks = group_chunks(ids, size=chunk)
    queue = get_queue(queue)
    for chunk in chunks:
        enqueue(queue, task, chunk)


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
    sub.add_argument('annotator', choices=ANNOTATORS)
    sub.add_argument('--offset', default=0, type=int)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=1000)

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if not args.function:
        parser.print_help()
        parser.exit()
    args.function(args)


if __name__ == '__main__':
    main()
