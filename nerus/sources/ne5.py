
from corus import load_ne5 as load_

from nerus.const import (
    NE5,
    NE5_DIR,
)
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.span import Span
from nerus.markup import Markup
from nerus.adapt.ne5 import adapt

from .base import (
    register,
    SourceRecord,
    Source
)


class Ne5Span(Span):
    __attributes__ = ['index', 'type', 'start', 'stop', 'text']

    def __init__(self, index, type, start, stop, text):
        self.index = index
        self.type = type
        self.start = start
        self.stop = stop
        self.text = text

    def offset(self, delta):
        return Ne5Span(
            self.index, self.type,
            self.start + delta,
            self.stop + delta,
            self.text
        )

    @classmethod
    def from_corus(cls, record):
        return Ne5Span(*record)


class Ne5Markup(SourceRecord, Markup):
    __attributes__ = ['id', 'text', 'spans']
    __annotations__ = {
        'spans': [Ne5Span]
    }

    label = NE5

    def __init__(self, id, text, spans):
        self.id = id
        self.text = text
        self.spans = spans

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield Ne5Markup(
                self.id, sent.text,
                list(spans)
            )

    @property
    def adapted(self):
        return adapt(self)

    @classmethod
    def from_corus(cls, record):
        return Ne5Markup(
            record.id, record.text,
            [Ne5Span.from_corus(_) for _ in record.spans]
        )


def load(dir=NE5_DIR):
    for record in load_(dir):
        yield Ne5Markup.from_corus(record)


class Ne5Source(Source):
    name = NE5
    load = staticmethod(load)


register(NE5, Ne5Markup, Ne5Source)
