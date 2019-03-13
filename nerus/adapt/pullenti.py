
from nerus.const import (
    PER,
    ORG,
    LOC
)
from nerus.span import (
    filter_empty_spans,
    strip_spans
)
from nerus.markup import Markup

from .common import (
    QUOTES,
    adapt_spans as adapt_spans_,
    adapt_overlapping_spans
)


TYPES = {
    'PERSON': PER,  # 11391
    'ORGANIZATION': ORG,  # 9723
    'GEO': LOC,  # 7234
    'STREET': LOC,  # 41
    'ADDRESS': LOC,  # 7

    # 'PERSONPROPERTY',  # 8350
    # 'MISSING',  # 43
}

BRACKETS = '()'
DASHES = '-'


def adapt_spans(spans, text):
    spans = list(adapt_overlapping_spans(spans, text))
    spans = list(strip_spans(spans, text, QUOTES + BRACKETS + DASHES))
    spans = list(filter_empty_spans(spans))
    return adapt_spans_(list(spans), text, TYPES)


def adapt(markup):
    spans = adapt_spans(list(markup.spans), markup.text)
    return Markup(markup.text, list(spans))
