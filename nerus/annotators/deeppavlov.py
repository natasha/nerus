
from itertools import groupby

from nerus.const import (
    DEEPPAVLOV,
    DEEPPAVLOV_HOST,
    DEEPPAVLOV_PORT,
    DEEPPAVLOV_SECTION,
    DEEPPAVLOV_BATCH,

    DEEPPAVLOV_CONTAINER_PORT,
    DEEPPAVLOV_IMAGE,
    DEEPPAVLOV_URL,
)
from nerus.utils import (
    Record,
    strict_zip,
    group_chunks
)
from nerus.token import (
    find_tokens,
    space_tokenize
)
from nerus.bio import bio_spans
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.span import offset_spans
from nerus.adapt.deeppavlov import adapt

from .base import (
    register,
    AnnotatorMarkup,
    ChunkAnnotator,
    ContainerAnnotator
)


class DeeppavlovMarkup(AnnotatorMarkup):
    label = DEEPPAVLOV

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield DeeppavlovMarkup(
                sent.text,
                list(spans)
            )

    @property
    def adapted(self):
        return adapt(self)


class Section(Record):
    __attributes__ = ['source', 'start', 'stop', 'text']

    def __init__(self, source, start, stop, text, markup=None):
        self.source = source
        self.start = start
        self.stop = stop
        self.text = text

    def annotated(self, spans):
        return AnnotatedSection(
            self.source, self.start, self.stop,
            self.text, spans
        )


class AnnotatedSection(Section):
    __attributes__ = ['source', 'start', 'stop', 'text', 'spans']

    def __init__(self, source, start, stop, text, spans):
        Section.__init__(self, source, start, stop, text)
        self.spans = spans


def section_texts(texts, size):
    for source, text in enumerate(texts):
        tokens = space_tokenize(text)
        chunks = group_chunks(tokens, size)
        for chunk in chunks:
            start, stop = chunk[0].start, chunk[-1].stop
            yield Section(
                source, start, stop,
                text[start:stop]
            )


def group_sections(sections):
    for _, group in groupby(sections, key=lambda _: _.source):
        yield group


def merge_markups(sections):
    chunks = []
    spans = []
    stop = 0
    for section in sections:
        chunks.append(' ' * (section.start - stop))
        chunks.append(section.text)
        spans.extend(offset_spans(section.spans, section.start))
        stop = section.stop
    text = ''.join(chunks)
    return DeeppavlovMarkup(text, spans)


DEEPPAVLOV_STRIP = '\t\r\n '  # \xa0 in tokens


def parse(texts, data):
    for text, (chunks, tags) in strict_zip(texts, data):
        # see patch_texts
        if not text.strip():
            spans = []
        else:
            tokens = list(find_tokens(chunks, text, strip=DEEPPAVLOV_STRIP))
            spans = list(bio_spans(tokens, tags))
        yield DeeppavlovMarkup(text, spans)


def post(texts, host, port):
    import requests

    url = DEEPPAVLOV_URL.format(
        host=host,
        port=port
    )
    payload = {'context': texts}
    response = requests.post(
        url,
        json=payload
    )
    response.raise_for_status()
    return response.json()


def patch_texts(texts):
    # deeppavlov does not work well with
    # texts=['', '\t', '   '] and so on
    for text in texts:
        if not text.strip():
            text = '?'  # assume ? is not tagged
        yield text


def map_(batches, host, port):
    for sections in batches:
        texts = [_.text for _ in sections]
        data = post(texts, host, port)
        markups = list(parse(texts, data))
        for section, markup in strict_zip(sections, markups):
            yield section.annotated(markup.spans)


def map(texts, host=DEEPPAVLOV_HOST, port=DEEPPAVLOV_PORT,
        section_size=DEEPPAVLOV_SECTION, batch_size=DEEPPAVLOV_BATCH):
    texts = patch_texts(texts)
    sections = section_texts(texts, section_size)
    batches = group_chunks(sections, batch_size)
    sections = map_(batches, host, port)
    groups = group_sections(sections)
    for group in groups:
        yield merge_markups(group)


class DeeppavlovAnnotator(ChunkAnnotator):
    name = DEEPPAVLOV
    host = DEEPPAVLOV_HOST
    port = DEEPPAVLOV_PORT

    section_size = DEEPPAVLOV_SECTION
    batch_size = DEEPPAVLOV_BATCH

    # BERT version starts >2min, requires >3GB
    retries = 100
    delay = 5

    def map(self, texts):
        return map(
            texts, self.host, self.port,
            self.section_size, self.batch_size
        )


class DeeppavlovContainerAnnotator(DeeppavlovAnnotator, ContainerAnnotator):
    image = DEEPPAVLOV_IMAGE
    container_port = DEEPPAVLOV_CONTAINER_PORT


register(
    DEEPPAVLOV,
    DeeppavlovMarkup,
    DeeppavlovAnnotator,
    DeeppavlovContainerAnnotator
)
