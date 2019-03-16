
import pytest

from nerus.const import PER, LOC, B, I, O
from nerus.token import Token
from nerus.span import Span
from nerus.bio import (
    format_bio,
    bio_spans,
    spans_bio,
    io_spans,
    spans_io
)


T1 = Token(0, 1, '1')
T2 = Token(2, 3, '2')
T3 = Token(4, 5, '3')

P1 = Span(0, 1, PER)
P2 = Span(2, 3, PER)
P12 = Span(0, 3, PER)
L2 = Span(2, 3, LOC)


PB = format_bio(B, PER)
PI = format_bio(I, PER)
LB = format_bio(B, LOC)
LI = format_bio(I, LOC)


TESTS = [
    [
        [T1, T2, T3],
        [],
        [O, O, O],
        [O, O, O]
    ],
    [
        [],
        [],
        [],
        []
    ],
    [
        [T1, T2, T3],
        [P1],
        [PB, O, O],
        [PI, O, O]
    ],
    [
        [T1, T2, T3],
        [P12],
        [PB, PI, O],
        [PI, PI, O]
    ],
    [
        [T1, T2, T3],
        [P1, L2],
        [PB, LB, O],
        [PI, LI, O]
    ],
    [
        [T1, T2],
        [P12],
        [PB, PI],
        [PI, PI]
    ],
]

BIO_TESTS = [
    [
        [T1, T2, T3],
        [P1, P2],
        [PB, PB, O],
        None
    ],
]


@pytest.mark.parametrize('test', TESTS + BIO_TESTS)
def test_bio(test):
    tokens, etalon_spans, etalon_tags, _ = test
    tags = list(spans_bio(tokens, etalon_spans))
    assert tags == etalon_tags

    spans = list(bio_spans(tokens, tags))
    assert spans == etalon_spans


@pytest.mark.parametrize('test', TESTS)
def test_io(test):
    tokens, etalon_spans, _, etalon_tags = test
    tags = list(spans_io(tokens, etalon_spans))
    assert tags == etalon_tags

    spans = list(io_spans(tokens, tags))
    assert spans == etalon_spans
