
from corus import load_lenta as load_

from nerus.const import (
    LENTA,
    LENTA_FILENAME,
    LENTA_URL,

    SOURCES_DIR
)
from nerus.etl import download
from nerus.path import (
    exists,
    join_path
)
from nerus.sent import sentenize

from .base import (
    register,
    SourceRecord,
    Source
)


class LentaRecord(SourceRecord):
    __attributes__ = ['url', 'title', 'text', 'topic', 'tags']

    label = LENTA

    def __init__(self, url, title, text, topic, tags):
        self.url = url
        self.title = title
        self.text = text
        self.topic = topic
        self.tags = tags

    @property
    def sents(self):
        for sent in sentenize(self.text):
            yield LentaRecord(
                self.url, self.title,
                sent.text,
                self.topic, self.tags
            )

    @classmethod
    def from_corus(cls, record):
        return LentaRecord(*record)


def load(path):
    for record in load_(path):
        yield LentaRecord.from_corus(record)


def get():
    path = join_path(SOURCES_DIR, LENTA_FILENAME)
    if exists(path):
        return path

    download(LENTA_URL, path)
    return path


class LentaSource(Source):
    name = LENTA
    get = staticmethod(get)
    load = staticmethod(load)


register(LENTA, LentaRecord, LentaSource)
