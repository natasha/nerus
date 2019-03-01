
import re

from nerus.path import (
    list_dir,
    join_path
)
from nerus.const import NE5
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.io import load_lines
from nerus.utils import Record


class Ne5Span(Record):
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


class Ne5Markup(Record):
    __attributes__ = ['id', 'text', 'spans']
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


def load(id, dir):
    path = txt_path(id, dir)
    text = load_text(path)
    path = ann_path(id, dir)
    lines = load_lines(path)
    spans = list(parse_spans(lines))
    return Ne5Markup(id, text, spans)
