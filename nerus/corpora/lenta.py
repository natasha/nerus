
from nerus.utils import Record
from nerus.const import (
    LENTA,
    LENTA_FILENAME,
    LENTA_URL,

    CORPORA_DIR
)
from nerus.etl import (
    download,
    load_gz_lines,
    parse_csv
)
from nerus.path import (
    exists,
    join_path
)


class LentaRecord(Record):
    __attributes__ = ['url', 'title', 'text', 'topic', 'tags']
    label = LENTA

    def __init__(self, url, title, text, topic, tags):
        self.url = url
        self.title = title
        self.text = text
        self.topic = topic
        self.tags = tags


def parse(lines):
    rows = parse_csv(lines)
    for cells in rows:
        yield LentaRecord(*cells)


def load(path):
    lines = load_gz_lines(path)
    return parse(lines)


def get():
    path = join_path(CORPORA_DIR, LENTA_FILENAME)
    if exists(path):
        return path

    download(LENTA_URL, path)
    return path
