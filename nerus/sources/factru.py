
import re

from nerus.path import (
    join_path,
    list_dir,
    exists,
    basename,
    rm
)
from nerus.etl import (
    load_text,
    load_lines,
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


def list_ids(dir, set):
    for filename in list_dir(join_path(dir, set)):
        match = re.match(r'^book_(\d+)\.txt$', filename)
        if match:
            yield match.group(1)


def txt_path(id, dir, set):
    return join_path(dir, set, 'book_%s.txt' % id)


def spans_path(id, dir, set):
    return join_path(dir, set, 'book_%s.spans' % id)


def objects_path(id, dir, set):
    return join_path(dir, set, 'book_%s.objects' % id)


def parse_spans(lines):
    for line in lines:
        id, type, start, size, _ = line.split(None, 4)
        start = int(start)
        stop = start + int(size)
        yield FactruSpan(id, type, start, stop)


def parse_objects(lines, spans):
    id_spans = {_.id: _ for _ in spans}
    for line in lines:
        parts = iter(line.split())
        id = next(parts)
        type = next(parts)
        spans = []
        for index in parts:
            if not index.isdigit():
                break
            span = id_spans[index]
            spans.append(span)
        yield FactruObject(id, type, spans)


def load_id(id, dir, set):
    path = txt_path(id, dir, set)
    text = load_text(path)
    path = spans_path(id, dir, set)
    lines = load_lines(path)
    spans = list(parse_spans(lines))
    path = objects_path(id, dir, set)
    lines = load_lines(path)
    objects = list(parse_objects(lines, spans))
    return FactruMarkup(id, text, objects)


def load(dir=FACTRU_DIR, sets=[FACTRU_DEVSET, FACTRU_TESTSET]):
    for set in sets:
        for id in list_ids(dir, set):
            yield load_id(id, dir, set)


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
