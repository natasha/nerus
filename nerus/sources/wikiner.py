
from corus import load_wikiner as load_

from nerus.const import (
    WIKINER,
    WIKINER_URL,
    WIKINER_FILENAME,

    SOURCES_DIR
)
from nerus.etl import download
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.markup import Markup
from nerus.path import (
    exists,
    join_path
)
from nerus.span import Span
from nerus.adapt.wikiner import adapt

from .base import (
    register,
    SourceRecord,
    Source
)


class WikinerMarkup(Markup, SourceRecord):
    label = WIKINER

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield WikinerMarkup(
                sent.text,
                list(spans)
            )

    @property
    def adapted(self):
        return adapt(self)

    @classmethod
    def from_corus(cls, record):
        return WikinerMarkup(
            record.text,
            [Span(*_) for _ in record.spans]
        )


def load(path):
    for record in load_(path):
        yield WikinerMarkup.from_corus(record)


def get():
    path = join_path(SOURCES_DIR, WIKINER_FILENAME)
    if exists(path):
        return path

    download(WIKINER_URL, path)
    return path


class WikinerSource(Source):
    name = WIKINER
    get = staticmethod(get)
    load = staticmethod(load)


register(WIKINER, WikinerMarkup, WikinerSource)
