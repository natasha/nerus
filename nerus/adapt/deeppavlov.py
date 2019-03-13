
from nerus.const import (
    LOC,
    ORG,
    PER
)

from .common import adapt as adapt_


TYPES = {
    'LOC': LOC,
    'ORG': ORG,
    'PER': PER,
}


def adapt(markup):
    return adapt_(markup, TYPES)
