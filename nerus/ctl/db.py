
from nerus.utils import (
    head,
    skip,
)
from nerus.log import (
    log,
    log_progress
)
from nerus.sources import Source
from nerus.db import (
    get_db,
    chunk_insert,
)
from nerus.const import (
    SOURCE,
    ANNOTATORS,
    WORKER_HOST
)


def db_insert(args):
    db_insert_(args.source, args.offset, args.count, args.chunk)


def db_insert_(name, offset, count, chunk):
    log('Inserting source')
    source = Source.find(name)
    path = source.get()
    records = source.load(path)
    records = log_progress(records, total=count)
    records = head(skip(records, offset), count)

    db = get_db(host=WORKER_HOST)
    docs = (_.as_bson for _ in records)
    chunk_insert(db[SOURCE], docs, chunk)


def db_show(args):
    db_show_()


def db_show_():
    log('Counting docs')
    db = get_db(host=WORKER_HOST)
    for name in [SOURCE] + ANNOTATORS:
        count = db[name].estimated_document_count()
        print('{count:>10} {name}'.format(
            name=name,
            count=count
        ))
def dump_db(args):
    annotators = args.annotators or ANNOTATORS
    dump_db_(args.path, annotators, args.count, args.chunk)


def dump_db_(path, annotators, count, chunk):
    log('Dumping %s', ', '.join(annotators))
    db = get_db(host=WORKER_HOST)
    records = dump(db, annotators, count, chunk)
    records = log_progress(records, total=count)
    items = (_.as_json for _ in records)
    lines = serialize_jsonl(items)
    dump_gz_lines(lines, path)
