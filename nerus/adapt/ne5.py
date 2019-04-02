
from nerus.const import (
    LOC,
    ORG,
    PER
)
from nerus.span import filter_overlapping
from nerus.markup import Markup

from .common import adapt_spans


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
    spans = list(filter_overlapping(markup.spans))
    spans = list(adapt_spans(spans, markup.text, TYPES))
    return Markup(markup.text, spans)
