
import pytest

from nerus.token import (
    Token,
    find_tokens
)


TESTS = [
    [
        ['a', 'b', 'c'],
        'a  b c',
        [
            Token(start=0, stop=1, text='a'),
            Token(start=3, stop=4, text='b'),
            Token(start=5, stop=6, text='c')
        ]
    ],
    [
        ['dr', 'johns'],
        'dr. johns',
        [
            Token(start=0, stop=2, text='dr'),
            Token(start=3, stop=8, text='johns')
        ]
    ],
    [
        ["''", 'a', "''"],
        '"a "',
        [
            Token(start=0, stop=1, text='"'),
            Token(start=1, stop=2, text='a'),
            Token(start=3, stop=4, text='"')
        ]
    ],
    [
        ['"', 'a', '"'],
        '"a"',
        [
            Token(start=0, stop=1, text='"'),
            Token(start=1, stop=2, text='a'),
            Token(start=2, stop=3, text='"')
        ]
    ],
    [
        ['O', "'Riley"],
        'O`Riley',
        [
            Token(start=0, stop=1, text='O'),
            Token(start=1, stop=7, text='`Riley')
        ]
    ],
]


@pytest.mark.parametrize('chunks, text, etalon', TESTS)
def test_find_tokens(chunks, text, etalon):
    guess = list(find_tokens(chunks, text))
    assert guess == etalon
