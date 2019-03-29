
from nerus.const import (
    WIKINER,
    WIKINER_URL,
    WIKINER_FILENAME,

    SOURCES_DIR
)
from nerus.etl import (
    load_bz2_lines,
    download
)
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.markup import Markup
from nerus.path import (
    exists,
    join_path
)
from nerus.token import find_tokens
from nerus.bio import io_spans
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


def parse(line):
    if not line:
        # skip empy lines
        return

    # На|PR|O севере|S|O граничит|V|O с|PR|O Латвией|S|I-LOC
    chunks = []
    tags = []
    for part in line.split():
        chunk, pos, tag = part.split('|', 2)
        chunks.append(chunk)
        tags.append(tag)
    text = ' '.join(chunks)
    tokens = list(find_tokens(chunks, text))
    spans = list(io_spans(tokens, tags))
    return WikinerMarkup(text, spans)


def load(path):
    lines = load_bz2_lines(path)
    for line in lines:
        record = parse(line)
        if record:
            yield record


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
