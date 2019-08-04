
from nerus.const import (
    PER,
    LOC,
    ORG
)
from nerus.span import strip_spans_bounds
from nerus.markup import Markup

from .common import (
    QUOTES, SPACES,
    adapt_spans
)


TYPES = {
    'PER': PER,
    'LOC': LOC,
    'ORG': ORG,
    # MISC drop
}


def adapt(markup):
    # большевистской газете " Правда " .
    #                       ----------
    spans = strip_spans_bounds(markup.spans, markup.text, QUOTES + SPACES)
    spans = adapt_spans(spans, markup.text, TYPES)
    return Markup(markup.text, list(spans))
