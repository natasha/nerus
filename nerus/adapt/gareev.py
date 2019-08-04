
from nerus.const import (
    PER,
    ORG
)
from nerus.span import (
    strip_spans,
    strip_spans_bounds
)
from nerus.markup import Markup

from .common import (
    QUOTES, SPACES, DOT,
    adapt_spans
)


TYPES = {
    'PER': PER,
    'ORG': ORG,
}


def adapt(markup):
    # extra spaces + dots in spans

    # News Corp .
    # -----------

    # « Русал »
    # ---------

    spans = strip_spans(markup.spans, markup.text, DOT + SPACES)
    spans = strip_spans_bounds(spans, markup.text, QUOTES + SPACES)
    spans = adapt_spans(spans, markup.text, TYPES)
    return Markup(markup.text, list(spans))
