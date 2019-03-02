
from nerus.log import log_progress
from nerus.const import (
    FACTRU,
    NE5,
    LENTA
)
from nerus.corpora import (
    factru,
    ne5,
    lenta
)
from nerus.worker import (
    get_db,
    insert_corpus,
    run as run__
)


CORPORA = {
    FACTRU: factru,
    NE5: ne5,
    LENTA: lenta
}


def insert(args):
    insert_(args.corpus)


def insert_(corpus):
    corpus = CORPORA[corpus]
    path = corpus.get()
    records = corpus.load(path)
    records = log_progress(records)

    db = get_db()
    insert_corpus(db, records)


def run(args):
    run_()


def run_():
    db = get_db()
    run__(db)
