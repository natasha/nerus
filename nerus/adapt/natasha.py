
from nerus.const import (
    PER,
    LOC,
    ORG
)
from nerus.markup import Markup

from .common import (
    adapt_spans as adapt_spans_,
    adapt_overlapping_spans
)


TYPES = {
    'Name': PER,  # 10039
    'Location': LOC,  # 9077
    'Organisation': ORG,  # 4158
}


def adapt_spans(spans, text):
    spans = list(adapt_overlapping_spans(spans, text))
    return adapt_spans_(list(spans), text, TYPES)


def adapt(markup):
    spans = adapt_spans(list(markup.spans), markup.text)
    return Markup(markup.text, list(spans))
