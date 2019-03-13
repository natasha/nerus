
from nerus.const import (
    PER,
    LOC,
    ORG
)

from .common import adapt as adapt_


TYPES = {
    'Name': PER,  # 10039
    'Location': LOC,  # 9077
    'Organisation': ORG,  # 4158
}


def adapt(markup):
    return adapt_(markup, TYPES)
