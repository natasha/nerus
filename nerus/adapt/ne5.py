
from nerus.const import (
    LOC,
    ORG,
    PER
)
from nerus.span import (
    filter_overlapping,
    strip_spans_bounds
)
from nerus.markup import Markup

from .common import (
    QUOTES,
    adapt_spans
)


TYPES = {
    'GEOPOLIT': LOC,
    'LOC': LOC,
    'MEDIA': ORG,
    'ORG': ORG,
    'PER': PER,
}


def adapt(markup):
    # ne5 bug
    #   Бражский район Подмосковья
    #   --------------
    #            -----------------

    # компания "Союзкалий"
    #          -----------

    spans = list(filter_overlapping(markup.spans))
    spans = strip_spans_bounds(spans, markup.text, QUOTES)
    spans = adapt_spans(spans, markup.text, TYPES)
    return Markup(markup.text, list(spans))
