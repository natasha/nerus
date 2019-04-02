
from nerus.const import (
    PER,
    LOC,
    ORG
)
from nerus.span import filter_overlapping
from nerus.markup import Markup

from .common import adapt_spans


TYPES = {
    'Name': PER,  # 10039
    'Location': LOC,  # 9077
    'Organisation': ORG,  # 4158
}


def adapt(markup):
    spans = list(markup.spans)
    spans = list(filter_overlapping(spans))
    spans = list(adapt_spans(spans, markup.text, TYPES))
    return Markup(markup.text, spans)
