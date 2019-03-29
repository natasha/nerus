
from nerus.const import (
    PER,
    ORG
)

from .common import adapt as adapt_


TYPES = {
    'PER': PER,
    'ORG': ORG,
}


def adapt(markup):
    return adapt_(markup, TYPES)
