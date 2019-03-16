
import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--int', action='store_true',
        help='run @pytest.mark.int tests'
    )


def pytest_runtest_setup(item):
    if 'int' in item.keywords and not item.config.getoption('--int'):
        pytest.skip('need --int option to run this test')
