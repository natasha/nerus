

import sys
import argparse

from nerus.const import (
    CORPUS,
    CORPORA,
    ANNOTATORS
)

from .db import (
    insert_corpus,
    db_stats,
    remove_collections
)
from .worker import (
    run_worker,
    show_worker,
    create_worker,
    deploy_worker,
    remove_worker,
    ssh_worker
)
from .queue import enqueue_tasks


def main():
    parser = argparse.ArgumentParser(prog='nerus-ctl')
    parser.set_defaults(function=None)

    subs = parser.add_subparsers()

    #######
    #  DB
    ########

    db = subs.add_parser('db').add_subparsers()

    sub = db.add_parser('insert')
    sub.set_defaults(function=insert_corpus)
    sub.add_argument('corpus', choices=CORPORA)
    sub.add_argument('--offset', type=int, default=0)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=1000)

    sub = db.add_parser('stats')
    sub.set_defaults(function=db_stats)

    sub = db.add_parser('rm')
    sub.set_defaults(function=remove_collections)
    sub.add_argument('collections', nargs='*', choices=ANNOTATORS + [CORPUS, []])

    ########
    #   WORKER
    #########

    worker = subs.add_parser('worker').add_subparsers()

    sub = worker.add_parser('run')
    sub.set_defaults(function=run_worker)

    sub = worker.add_parser('create')
    sub.set_defaults(function=create_worker)

    sub = worker.add_parser('deploy')
    sub.set_defaults(function=deploy_worker)

    sub = worker.add_parser('show')
    sub.set_defaults(function=show_worker)

    sub = worker.add_parser('ssh')
    sub.set_defaults(function=ssh_worker)
    sub.add_argument('command')

    sub = worker.add_parser('rm')
    sub.set_defaults(function=remove_worker)

    ########
    #  QUEUE
    #########

    sub = subs.add_parser('q')
    sub.set_defaults(function=enqueue_tasks)
    sub.add_argument('annotators', nargs='*', choices=ANNOTATORS + [[]])
    sub.add_argument('--offset', type=int, default=0)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=1000)
    sub.add_argument('--dry-run', action='store_true')

    ##########
    #   PARSE
    ########

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if not args.function:
        parser.print_help()
        parser.exit()
    args.function(args)
