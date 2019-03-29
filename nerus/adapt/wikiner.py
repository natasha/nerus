
from nerus.const import (
    PER,
    LOC,
    ORG
)

from .common import adapt as adapt_


TYPES = {
    'PER': PER,
    'LOC': LOC,
    'ORG': ORG,
    # MISC drop
}


def adapt(markup):
    return adapt_(markup, TYPES)
