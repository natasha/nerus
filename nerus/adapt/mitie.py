
from nerus.const import (
    LOC,
    ORG,
    PER
)

from .common import adapt as adapt_


TYPES = {
    'PERS': PER,
    'ORG': ORG,
    'LOC': LOC,
}


def adapt(markup):
    return adapt_(markup, TYPES)
