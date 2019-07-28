
from corus import load_gareev as load_

from nerus.const import (
    GAREEV,
    GAREEV_DIR,

    SOURCES_DIR
)
from nerus.path import (
    exists,
    join_path
)
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.markup import Markup
from nerus.span import Span
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

    @classmethod
    def from_corus(self, record):
        return GareevMarkup(
            record.text,
            [Span(*_) for _ in record.spans]
        )


def load(dir=GAREEV_DIR):
    for record in load_(dir):
        yield GareevMarkup.from_corus(record)


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
