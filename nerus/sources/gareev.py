
import re

from nerus.const import (
    GAREEV,
    GAREEV_DIR,

    SOURCES_DIR
)
from nerus.path import (
    exists,
    list_dir,
    join_path
)
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.etl import load_lines
from nerus.markup import Markup
from nerus.token import find_tokens
from nerus.bio import bio_spans
from nerus.adapt.gareev import adapt

from .base import (
    register,
    SourceRecord,
    Source
)


class GareevMarkup(Markup, SourceRecord):
    label = GAREEV

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield GareevMarkup(
                sent.text,
                list(spans)
            )

    @property
    def adapted(self):
        return adapt(self)


def parse_conll(lines):
    chunks = []
    tags = []
    for line in lines:
        chunk, tag = line.split('\t', 1)
        chunks.append(chunk)
        tags.append(tag)
    text = ' '.join(chunks)
    tokens = list(find_tokens(chunks, text))
    spans = list(bio_spans(tokens, tags))
    return GareevMarkup(text, spans)


def load_id(id, dir):
    path = join_path(dir, '%s.txt.iob' % id)
    lines = load_lines(path)
    return parse_conll(lines)


def list_ids(dir):
    for filename in list_dir(dir):
        match = re.match(r'^(.+).txt.iob', filename)
        if match:
            yield match.group(1)


def load(dir=GAREEV_DIR):
    for id in list_ids(dir):
        yield load_id(id, dir)


def get():
    dir = join_path(SOURCES_DIR, GAREEV_DIR)
    if not exists(dir):
        raise NotImplementedError(
            'Email Rinat Gareev <gareev-rm@yandex.ru> ask for dataset, '
            'tar -xvf rus-ner-news-corpus.iob.tar.gz, '
            'rm rus-ner-news-corpus.iob.tar.gz, '
            'mv rus-ner-news-corpus.iob data/sources'
        )
    return dir


class GareevSource(Source):
    name = GAREEV
    get = staticmethod(get)
    load = staticmethod(load)


register(GAREEV, GareevMarkup, GareevSource)
