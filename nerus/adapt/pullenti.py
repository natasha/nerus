
from nerus.const import (
    PER,
    ORG,
    LOC
)
from nerus.span import (
    filter_empty_spans,
    split_overlapping_spans,
    strip_spans
)
from nerus.markup import Markup

from .common import (
    QUOTES, SPACES,
    adapt_spans
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


def adapt(markup):
    spans = list(markup.spans)
    spans = list(split_overlapping_spans(spans))
    spans = list(strip_spans(spans, markup.text, QUOTES + BRACKETS + DASHES + SPACES))
    spans = list(filter_empty_spans(spans))
    spans = list(adapt_spans(spans, markup.text, TYPES))
    return Markup(markup.text, spans)
