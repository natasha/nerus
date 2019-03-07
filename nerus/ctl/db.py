
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
    get_stats as db_stats_
)
from nerus.const import (
    CORPUS,
    ANNOTATORS
)


def insert_corpus(args):
    insert_corpus_(args.corpus, args.offset, args.count, args.chunk)


def insert_corpus_(corpus, offset, count, chunk):
    schema = find_corpus(corpus)
    path = schema.get()
    corpus = schema.load(path)
    corpus = log_progress(corpus)
    corpus = head(skip(corpus, offset), count)

    db = get_db()
    log('Inserting corpus: %s', schema.name)
    docs = (_.as_bson for _ in corpus)
    chunk_insert(db[CORPUS], docs, chunk)


def db_stats(args):
    log('Getting stats')
    db = get_db()
    for count, name in db_stats_(db):
        print(count, name, sep='\t')


def remove_collections(args):
    collections = args.collections or ANNOTATORS + [CORPUS]
    remove_collections_(collections)


def remove_collections_(collections):
    db = get_db()
    for collection in collections:
        log('Removing %s' % collection)
        db[collection].remove()
