
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
    collection_counts as collection_counts_
)
from nerus.const import (
    CORPUS,
    ANNOTATORS,
    WORKER_HOST
)


def insert_corpus(args):
    insert_corpus_(args.corpus, args.offset, args.count, args.chunk)


def insert_corpus_(corpus, offset, count, chunk):
    log('Inserting corpus')
    schema = find_corpus(corpus)
    path = schema.get()
    corpus = schema.load(path)
    corpus = log_progress(corpus)
    corpus = head(skip(corpus, offset), count)

    db = get_db(host=WORKER_HOST)
    docs = (_.as_bson for _ in corpus)
    chunk_insert(db[CORPUS], docs, chunk)


def collection_counts(args):
    log('Counting docs')
    db = get_db(host=WORKER_HOST)
    for count, name in collection_counts_(db):
        print(count, name, sep='\t')


def remove_collections(args):
    collections = args.collections or ANNOTATORS + [CORPUS]
    remove_collections_(collections)


def remove_collections_(collections):
    db = get_db(host=WORKER_HOST)
    for collection in collections:
        log('Removing %s' % collection)
        db[collection].remove()
