
import pytest

from . import (
    test_factru,
    test_lenta,
    test_ne5
)


TESTS = (
    test_factru.ETALON
    + test_lenta.ETALON
    + test_ne5.ETALON
)


@pytest.mark.parametrize('etalon', TESTS)
def test_serialization(etalon):
    data = etalon.as_bson
    Record = type(etalon)
    guess = Record.from_bson(data)
    assert guess == etalon
