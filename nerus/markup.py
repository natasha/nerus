

from .utils import Record
from .sent import (
    sentenize,
    sent_spans
)


class Markup(Record):
    __attributes__ = ['id', 'text', 'spans']

    def __init__(self, id, text, spans):
        self.id = id
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
