

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

    @property
    def adapted(self):
        raise NotImplementedError


class Multimarkup(Markup):
    __attributes__ = ['text', 'markups']
    __annotations__ = {
        'markups': [Markup]
    }

    def __init__(self, text, markups):
        self.text = text
        self.markups = markups

    @property
    def sents(self):
        sents = sentenize(self.text)
        markups = (_.sents for _ in self.markups)
        for sent, *markups in zip(sents, *markups):
            yield Multimarkup(sent.text, markups)

    @property
    def adapted(self):
        return Multimarkup(
            self.text,
            [_.adapted for _ in self.markups]
        )

    @property
    def mixed(self):
        from .mix import mix
        return mix(self)

    @property
    def spans(self):
        return self.mixed.spans
