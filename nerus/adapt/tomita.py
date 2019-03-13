
from nerus.const import PER

from .common import adapt as adapt_


TYPES = {
    'PER': PER
}


def adapt(markup):
    return adapt_(markup, TYPES)
