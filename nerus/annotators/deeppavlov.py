
from nerus.const import (
    DEEPPAVLOV,
    DEEPPAVLOV_HOST,
    DEEPPAVLOV_PORT,
    DEEPPAVLOV_CHUNK,

    DEEPPAVLOV_CONTAINER_PORT,
    DEEPPAVLOV_IMAGE,
    DEEPPAVLOV_URL,
)
from nerus.utils import (
    strict_zip,
    group_weighted_chunks
)
from nerus.token import find_tokens
from nerus.bio import bio_spans
from nerus.sent import (
    sentenize,
    sent_spans
)
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


def parse(texts, data):
    for text, (chunks, tags) in strict_zip(texts, data):
        # see patch_texts
        if not text.strip():
            spans = []
        else:
            tokens = list(find_tokens(chunks, text))
            spans = list(bio_spans(tokens, tags))
        yield DeeppavlovMarkup(text, spans)


def post(texts, host, port):
    import requests

    url = DEEPPAVLOV_URL.format(
        host=host,
        port=port
    )
    payload = {'text1': texts}
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
            text = '?'  # assume ? is not tagger
        yield text


def map(texts, host=DEEPPAVLOV_HOST, port=DEEPPAVLOV_PORT, size=DEEPPAVLOV_CHUNK):
    texts = (_[:size] for _ in texts)
    chunks = group_weighted_chunks(texts, size, len)
    for chunk in chunks:
        patched = list(patch_texts(chunk))
        data = post(patched, host, port)
        for markup in parse(chunk, data):
            yield markup


class DeeppavlovAnnotator(ChunkAnnotator):
    name = DEEPPAVLOV
    host = DEEPPAVLOV_HOST
    port = DEEPPAVLOV_PORT
    chunk = DEEPPAVLOV_CHUNK

    def map(self, texts):
        return map(texts, self.host, self.port, self.chunk)


class DeeppavlovContainerAnnotator(DeeppavlovAnnotator, ContainerAnnotator):
    image = DEEPPAVLOV_IMAGE
    container_port = DEEPPAVLOV_CONTAINER_PORT


register(
    DEEPPAVLOV,
    DeeppavlovMarkup,
    DeeppavlovAnnotator,
    DeeppavlovContainerAnnotator
)
