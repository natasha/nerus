
from nerus.const import (
    LOC,
    ORG,
    PER
)
from nerus.span import strip_spans
from nerus.markup import Markup

from .common import (
    QUOTES, DOT, SPACES,
    adapt_spans
)


TYPES = {
    'PERS': PER,
    'ORG': ORG,
    'LOC': LOC,
}


def adapt(markup):
    # год Чарльза Дарвина»
    #     ----------------
    spans = list(strip_spans(markup.spans, markup.text, QUOTES + DOT + SPACES))
    spans = list(adapt_spans(spans, markup.text, TYPES))
    return Markup(markup.text, spans)
