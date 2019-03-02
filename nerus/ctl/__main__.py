
import sys
import argparse

from nerus.const import CORPORA

from .worker import (
    insert as worker_insert,
    run as worker_run,
)


def main():
    parser = argparse.ArgumentParser(prog='ctl')
    parser.set_defaults(function=None)

    subs = parser.add_subparsers()

    ######
    #   WORKER
    ########

    worker = subs.add_parser('worker').add_subparsers()

    sub = worker.add_parser('insert')
    sub.set_defaults(function=worker_insert)
    sub.add_argument('corpus', choices=CORPORA)

    sub = worker.add_parser('run')
    sub.set_defaults(function=worker_run)

    ########
    #   PARSE
    ##########

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if not args.function:
        parser.print_help()
        parser.exit()
    args.function(args)


if __name__ == '__main__':
    main()
