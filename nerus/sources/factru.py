
from corus import load_factru as load_

from nerus.path import (
    join_path,
    exists,
    basename,
    rm
)
from nerus.etl import (
    download,
    unzip,
)
from nerus.markup import Markup
from nerus.utils import Record
from nerus.const import (
    FACTRU,
    FACTRU_URL,
    FACTRU_DIR,
    FACTRU_TESTSET,
    FACTRU_DEVSET,

    SOURCES_DIR
)
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.span import (
    Span,
    offset_spans
)
from nerus.adapt.factru import adapt

from .base import (
    register,
    SourceRecord,
    Source
)


class FactruSpan(Span):
    __attributes__ = ['id', 'type', 'start', 'stop']

    def __init__(self, id, type, start, stop):
        self.id = id
        self.type = type
        self.start = start
        self.stop = stop

    def offset(self, delta):
        return FactruSpan(
            self.id, self.type,
            self.start + delta,
            self.stop + delta
        )

    @classmethod
    def from_corus(cls, record):
        return FactruSpan(*record)


class FactruObject(Record):
    __attributes__ = ['id', 'type', 'spans']
    __annotations__ = {
        'spans': [FactruSpan]
    }

    def __init__(self, id, type, spans):
        self.id = id
        self.type = type
        self.spans = spans

    def offset(self, delta):
        spans = offset_spans(self.spans, delta)
        return FactruObject(
            self.id, self.type,
            list(spans)
        )

    @property
    def start(self):
        return min(_.start for _ in self.spans)

    @property
    def stop(self):
        return max(_.stop for _ in self.spans)

    @classmethod
    def from_corus(cls, record):
        return FactruObject(
            record.id, record.type,
            [FactruSpan.from_corus(_) for _ in record.spans]
        )


class FactruMarkup(SourceRecord, Markup):
    __attributes__ = ['id', 'text', 'objects']
    __annotations__ = {
        'objects': [FactruObject]
    }

    label = FACTRU

    def __init__(self, id, text, objects):
        self.id = id
        self.text = text
        self.objects = objects

    @property
    def spans(self):
        for object in self.objects:
            for span in object.spans:
                label = span.type + '_' + object.id[-2:]
                yield Span(span.start, span.stop, label)
            label = object.type + '_' + object.id[-2:]
            yield Span(object.start, object.stop, label)

    @property
    def sents(self):
        for sent in sentenize(self.text):
            objects = sent_spans(sent, self.objects)
            yield FactruMarkup(
                self.id, sent.text,
                list(objects)
            )

    @property
    def adapted(self):
        return adapt(self)

    @classmethod
    def from_corus(cls, record):
        return FactruMarkup(
            record.id, record.text,
            [FactruObject.from_corus(_) for _ in record.objects]
        )


def load(dir=FACTRU_DIR, sets=[FACTRU_DEVSET, FACTRU_TESTSET]):
    for record in load_(dir, sets):
        yield FactruMarkup.from_corus(record)


def get():
    dir = join_path(SOURCES_DIR, FACTRU_DIR)
    if exists(dir):
        return dir

    path = join_path(SOURCES_DIR, basename(FACTRU_URL))
    download(FACTRU_URL, path)
    unzip(path, SOURCES_DIR)
    rm(path)

    return dir


class FactruSource(Source):
    name = FACTRU
    get = staticmethod(get)
    load = staticmethod(load)


register(FACTRU, FactruMarkup, FactruSource)
