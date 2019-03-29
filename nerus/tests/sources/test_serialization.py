
import pytest

from . import (
    test_factru,
    test_lenta,
    test_ne5,
    test_wikiner,
    test_gareev
)


TESTS = (
    test_factru.ETALON
    + test_lenta.ETALON
    + test_ne5.ETALON
    + test_wikiner.ETALON
    + test_gareev.ETALON
)


@pytest.mark.parametrize('etalon', TESTS)
def test_serialization(etalon):
    data = etalon.as_bson
    Record = type(etalon)
    guess = Record.from_bson(data)
    assert guess == etalon
