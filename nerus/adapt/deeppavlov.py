
from nerus.const import (
    LOC,
    ORG,
    PER
)
from nerus.span import strip_spans
from nerus.markup import Markup

from .common import (
    QUOTES, SPACES,
    adapt_spans
)


TYPES = {
    'LOC': LOC,
    'ORG': ORG,
    'PER': PER,
}


def adapt(markup):
    # "Ленфильм"
    #  ---------
    spans = list(strip_spans(markup.spans, markup.text, QUOTES + SPACES))
    spans = list(adapt_spans(spans, markup.text, TYPES))
    return Markup(markup.text, spans)
