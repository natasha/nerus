
from nerus.utils import (
    head,
    skip
)
from nerus.log import (
    log,
    log_progress
)
from nerus.corpora import find as find_corpus
from nerus.db import (
    get_db,
    chunk_insert,
)
from nerus.const import (
    CORPUS,
    ANNOTATORS,
    WORKER_HOST
)
from nerus.path import (
    exists,
    rm
)
from nerus.dump import (
    read_collection,
    encode_corpus,
    encode_annotator,
    dump_collection
)


def insert_corpus(args):
    insert_corpus_(args.corpus, args.offset, args.count, args.chunk)


def insert_corpus_(corpus, offset, count, chunk):
    log('Inserting corpus')
    schema = find_corpus(corpus)
    path = schema.get()
    corpus = schema.load(path)
    corpus = log_progress(corpus, total=count)
    corpus = head(skip(corpus, offset), count)

    db = get_db(host=WORKER_HOST)
    docs = (_.as_bson for _ in corpus)
    chunk_insert(db[CORPUS], docs, chunk)


def show_db(args):
    show_db_()


def show_db_():
    log('Counting docs')
    db = get_db(host=WORKER_HOST)
    for name in [CORPUS] + ANNOTATORS:
        count = db[name].estimated_document_count()
        print('{count:>10} {name}'.format(
            name=name,
            count=count
        ))


def remove_collections(args):
    collections = args.collections or ANNOTATORS + [CORPUS]
    remove_collections_(collections)


def remove_collections_(collections):
    db = get_db(host=WORKER_HOST)
    for collection in collections:
        log('Removing %s' % collection)
        db[collection].remove()


def dump_db(args):
    annotators = args.annotators or ANNOTATORS
    dump_db_(args.path, annotators, args.count, args.chunk)


def dump_db_(path, annotators, count, chunk):
    if exists(path):
        rm(path)

    log('Dumping')
    db = get_db(host=WORKER_HOST)
    docs = read_collection(db[CORPUS], count, chunk)
    docs = encode_corpus(docs)
    docs = log_progress(docs, prefix=CORPUS, total=count)
    dump_collection(path, CORPUS, docs)

    for annotator in annotators:
        docs = read_collection(db[annotator], count, chunk)
        docs = encode_annotator(docs)
        docs = log_progress(docs, prefix=annotator, total=count)
        dump_collection(path, annotator, docs)
    log('Dump: %s' % path)
