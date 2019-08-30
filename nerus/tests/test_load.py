
from nerus.path import (
    join_path,
    get_dir
)
from nerus.load import (
    load_nerus,
    load_raw_nerus
)
from nerus.const import DEEPPAVLOV
from nerus.span import Span


DATA_DIR = join_path(get_dir(__file__), 'data')
# cat data/dumps/lenta.raw.jsonl.gz | gunzip | head -1 | gzip > nerus/tests/data/test.raw.jsonl.gz
# cat data/dumps/lenta.jsonl.gz | gunzip | head -1 | gzip > nerus/tests/data/test.jsonl.gz
RAW = join_path(DATA_DIR, 'test.raw.jsonl.gz')
NORM = join_path(DATA_DIR, 'test.jsonl.gz')

SPANS = [
    Span(start=36, stop=52, type='PER'),
    Span(start=82, stop=88, type='LOC'),
    Span(start=149, stop=160, type='ORG'),
    Span(start=172, stop=181, type='PER'),
    Span(start=251, stop=260, type='LOC'),
    Span(start=262, stop=270, type='LOC'),
    Span(start=272, stop=280, type='LOC'),
    Span(start=283, stop=301, type='LOC'),
    Span(start=313, stop=324, type='LOC'),
    Span(start=383, stop=389, type='LOC'),
    Span(start=560, stop=568, type='ORG')
]


def test_load_raw():
    record = next(load_raw_nerus(RAW))
    assert record.find(DEEPPAVLOV).spans == SPANS


def test_load_norm():
    record = next(load_nerus(NORM))
    assert record.spans == SPANS
