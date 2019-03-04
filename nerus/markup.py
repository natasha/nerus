

from .utils import Record
from .span import Span
from .sent import (
    sentenize,
    sent_spans
)


class Markup(Record):
    __attributes__ = ['text', 'spans']
    __annotations__ = {
        'spans': [Span]
    }

    def __init__(self, text, spans):
        self.text = text
        self.spans = spans

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield Markup(
                sent.text,
                list(spans)
            )
