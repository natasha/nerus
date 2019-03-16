
from nerus.log import (
    log,
    log_progress
)
from nerus.const import (
    WORKER_HOST,
    ANNOTATORS
)
from nerus.db import get_db
from nerus.dump import (
    read_raw,
    dump_raw as dump_raw__,
    load_raw,
    norm_raw,
    dump_norm as dump_norm__
)


def dump_raw(args):
    annotators = args.annotators or ANNOTATORS
    dump_raw_(args.path, annotators, args.count, args.chunk)


def dump_raw_(path, annotators, count, chunk):
    log('Dumping %s', ', '.join(annotators))
    db = get_db(host=WORKER_HOST)
    records = read_raw(db, annotators, count, chunk)
    records = log_progress(records, total=count)
    dump_raw__(records, path)


def dump_norm(args):
    dump_norm_(args.source, args.target)


def dump_norm_(source, target):
    records = load_raw(source)
    records = norm_raw(records)
    records = log_progress(records)
    dump_norm__(records, target)
