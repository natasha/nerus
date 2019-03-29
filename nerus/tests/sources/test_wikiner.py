
from nerus.path import (
    join_path,
    get_dir
)
from nerus.const import WIKINER_FILENAME
from nerus.span import Span
from nerus.sources.wikiner import (
    WikinerMarkup,
    WikinerSource
)


DATA_DIR = join_path(get_dir(__file__), 'data')
ETALON = [
    WikinerMarkup(text='На севере граничит с Латвией , на востоке -- с Белоруссией , на юго-западе -- c Польшей и Калининградской областью России .', spans=[Span(start=21, stop=28, type='LOC'), Span(start=47, stop=58, type='LOC'), Span(start=80, stop=87, type='LOC'), Span(start=90, stop=114, type='LOC'), Span(start=115, stop=121, type='LOC')])
]


def test_load():
    path = join_path(DATA_DIR, WIKINER_FILENAME)
    guess = list(WikinerSource.load(path))
    assert guess == ETALON
