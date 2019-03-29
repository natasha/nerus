
import re

from nerus.path import (
    list_dir,
    join_path,
    exists,
    basename,
    rm
)
from nerus.const import (
    NE5,
    NE5_DIR,
    NE5_URL,

    SOURCES_DIR
)
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.etl import (
    load_lines,
    download,
    unzip
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


def list_ids(dir):
    for filename in list_dir(dir):
        match = re.match(r'^(.+).txt$', filename)
        if match:
            yield match.group(1)


def txt_path(id, dir):
    return join_path(dir, '%s.txt' % id)


def ann_path(id, dir):
    return join_path(dir, '%s.ann' % id)


def parse_spans(lines):
    # brat format http://brat.nlplab.org/standoff.html
    for line in lines:
        index, type, start, stop, text = line.split(None, 4)
        start = int(start)
        stop = int(stop)
        yield Ne5Span(index, type, start, stop, text)


def load_text(path):
    # do not convert \r\n to \n
    with open(path, newline='') as file:
        return file.read()


def load_id(id, dir):
    path = txt_path(id, dir)
    text = load_text(path)
    path = ann_path(id, dir)
    lines = load_lines(path)
    spans = list(parse_spans(lines))
    return Ne5Markup(id, text, spans)


def load(dir=NE5_DIR):
    for id in list_ids(dir):
        yield load_id(id, dir)


def get():
    dir = join_path(SOURCES_DIR, NE5_DIR)
    if exists(dir):
        return dir

    path = join_path(SOURCES_DIR, basename(NE5_URL))
    download(NE5_URL, path)
    unzip(path, SOURCES_DIR)
    rm(path)

    return dir


class Ne5Source(Source):
    name = NE5
    get = staticmethod(get)
    load = staticmethod(load)


register(NE5, Ne5Markup, Ne5Source)
