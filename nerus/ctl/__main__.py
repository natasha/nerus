

import sys
import argparse

from nerus.const import (
    SOURCE,
    SOURCES,
    ANNOTATORS
)


# a bit quicker startup

def insert_source(*args): from .db import insert_source as f; return f(*args)
def show_db(*args): from .db import show_db as f; return f(*args)
def remove_collections(*args): from .db import remove_collections as f; return f(*args)
def dump_db(*args): from .db import dump_db as f; return f(*args)

def run_worker(*args): from .worker import run_worker as f; return f(*args)
def worker_ip(*args): from .worker import worker_ip as f; return f(*args)
def create_worker(*args): from .worker import create_worker as f; return f(*args)
def deploy_worker(*args): from .worker import deploy_worker as f; return f(*args)
def remove_worker(*args): from .worker import remove_worker as f; return f(*args)
def ssh_worker(*args): from .worker import ssh_worker as f; return f(*args)
def worker_upload(*args): from .worker import worker_upload as f; return f(*args)
def worker_download(*args): from .worker import worker_download as f; return f(*args)

def enqueue_tasks(*args): from .queue import enqueue_tasks as f; return f(*args)
def show_queues(*args): from .queue import show_queues as f; return f(*args)
def show_failed(*args): from .queue import show_failed as f; return f(*args)
def retry_failed(*args): from .queue import retry_failed as f; return f(*args)


def main():
    parser = argparse.ArgumentParser(prog='nerus-ctl')
    parser.set_defaults(function=None)

    subs = parser.add_subparsers()

    ########
    #   WORKER
    #########

    worker = subs.add_parser('worker').add_subparsers()

    sub = worker.add_parser('run')
    sub.set_defaults(function=run_worker)

    sub = worker.add_parser('create')
    sub.set_defaults(function=create_worker)

    sub = worker.add_parser('ip')
    sub.set_defaults(function=worker_ip)

    sub = worker.add_parser('ssh')
    sub.set_defaults(function=ssh_worker)
    sub.add_argument('command')

    sub = worker.add_parser('upload')
    sub.set_defaults(function=worker_upload)
    sub.add_argument('source')
    sub.add_argument('target', nargs='?')

    sub = worker.add_parser('download')
    sub.set_defaults(function=worker_download)
    sub.add_argument('source')
    sub.add_argument('target', nargs='?')

    sub = worker.add_parser('rm')
    sub.set_defaults(function=remove_worker)

    #######
    #  DB
    ########

    db = subs.add_parser('db').add_subparsers()

    sub = db.add_parser('insert')
    sub.set_defaults(function=insert_source)
    sub.add_argument('source', choices=SOURCES)
    sub.add_argument('--offset', type=int, default=0)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=1000)

    sub = db.add_parser('show')
    sub.set_defaults(function=show_db)

    sub = db.add_parser('rm')
    sub.set_defaults(function=remove_collections)
    # https://utcc.utoronto.ca/~cks/space/blog/python/ArgparseNargsChoicesLimitation
    sub.add_argument('collections', nargs='*', choices=[[]] + ANNOTATORS + [SOURCE])

    sub = db.add_parser('dump')
    sub.set_defaults(function=dump_db)
    sub.add_argument('path')
    sub.add_argument('annotators', nargs='*', choices=[[]] + ANNOTATORS)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=10000)

    ########
    #  QUEUE
    #########

    queue = subs.add_parser('q').add_subparsers()

    sub = queue.add_parser('insert')
    sub.set_defaults(function=enqueue_tasks)
    sub.add_argument('annotators', nargs='*', choices=[[]] + ANNOTATORS)
    sub.add_argument('--offset', type=int, default=0)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=100)
    sub.add_argument('--dry-run', action='store_true')

    sub = queue.add_parser('show')
    sub.set_defaults(function=show_queues)

    sub = queue.add_parser('failed')
    sub.set_defaults(function=show_failed)

    sub = queue.add_parser('retry')
    sub.set_defaults(function=retry_failed)

    ##########
    #   PARSE
    ########

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if not args.function:
        parser.print_help()
        parser.exit()
    try:
        args.function(args)
    except KeyboardInterrupt:
        pass
