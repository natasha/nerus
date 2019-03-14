

import sys
import argparse

from nerus.const import (
    SOURCES,
    ANNOTATORS
)


# a bit quicker startup

def worker_run(*args): from .worker import worker_run as f; return f(*args)
def worker_ip(*args): from .worker import worker_ip as f; return f(*args)
def worker_create(*args): from .worker import worker_create as f; return f(*args)
def worker_deploy(*args): from .worker import worker_deploy as f; return f(*args)
def worker_remove(*args): from .worker import worker_remove as f; return f(*args)
def worker_ssh(*args): from .worker import worker_ssh as f; return f(*args)
def worker_upload(*args): from .worker import worker_upload as f; return f(*args)
def worker_download(*args): from .worker import worker_download as f; return f(*args)

def db_insert(*args): from .db import db_insert as f; return f(*args)
def db_show(*args): from .db import db_show as f; return f(*args)

def queue_insert(*args): from .queue import queue_insert as f; return f(*args)
def queue_show(*args): from .queue import queue_show as f; return f(*args)
def queue_failed(*args): from .queue import queue_failed as f; return f(*args)
def queue_retry(*args): from .queue import queue_retry as f; return f(*args)

def dump_raw(*args): from .dump import dump_raw as f; return f(*args)
def dump_norm(*args): from .dump import dump_norm as f; return f(*args)


def main():
    parser = argparse.ArgumentParser(prog='nerus-ctl')
    parser.set_defaults(function=None)

    subs = parser.add_subparsers()

    ########
    #   WORKER
    #########

    worker = subs.add_parser('worker').add_subparsers()

    sub = worker.add_parser('run')
    sub.set_defaults(function=worker_run)

    sub = worker.add_parser('create')
    sub.set_defaults(function=worker_create)

    sub = worker.add_parser('ip')
    sub.set_defaults(function=worker_ip)

    sub = worker.add_parser('ssh')
    sub.set_defaults(function=worker_ssh)
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
    sub.set_defaults(function=worker_remove)

    #######
    #  DB
    ########

    db = subs.add_parser('db').add_subparsers()

    sub = db.add_parser('insert')
    sub.set_defaults(function=db_insert)
    sub.add_argument('source', choices=SOURCES)
    sub.add_argument('--offset', type=int, default=0)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=1000)

    sub = db.add_parser('show')
    sub.set_defaults(function=db_show)

    ########
    #  QUEUE
    #########

    queue = subs.add_parser('q').add_subparsers()

    sub = queue.add_parser('insert')
    sub.set_defaults(function=queue_insert)
    sub.add_argument('annotators', nargs='*', choices=[[]] + ANNOTATORS)
    sub.add_argument('--offset', type=int, default=0)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=100)

    sub = queue.add_parser('show')
    sub.set_defaults(function=queue_show)

    sub = queue.add_parser('failed')
    sub.set_defaults(function=queue_failed)

    sub = queue.add_parser('retry')
    sub.set_defaults(function=queue_retry)
    sub.add_argument('--chunk', type=int, default=100)

    #########
    #  DUMP
    ##########

    dump = subs.add_parser('dump').add_subparsers()

    sub = dump.add_parser('raw')
    sub.set_defaults(function=dump_raw)
    sub.add_argument('path')
    sub.add_argument('annotators', nargs='*', choices=[[]] + ANNOTATORS)
    sub.add_argument('--count', type=int)
    sub.add_argument('--chunk', type=int, default=10000)

    sub = dump.add_parser('norm')
    sub.set_defaults(function=dump_norm)
    sub.add_argument('source')
    sub.add_argument('target')

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
