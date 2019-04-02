
from nerus.const import (
    PER,
    ORG
)
from nerus.span import strip_spans
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
    spans = strip_spans(markup.spans, markup.text, QUOTES + SPACES + DOT)
    spans = adapt_spans(spans, markup.text, TYPES)
    return Markup(markup.text, list(spans))
