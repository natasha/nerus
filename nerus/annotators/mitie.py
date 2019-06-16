
from nerus.const import (
    MITIE,
    MITIE_HOST,
    MITIE_PORT,

    MITIE_CONTAINER_PORT,
    MITIE_IMAGE,
    MITIE_URL,
)
from nerus.token import find_tokens
from nerus.span import Span
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.adapt.mitie import adapt

from .base import (
    register,
    AnnotatorMarkup,
    Annotator,
    ContainerAnnotator
)


class MitieMarkup(AnnotatorMarkup):
    label = MITIE

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield MitieMarkup(sent.text, list(spans))

    @property
    def adapted(self):
        return adapt(self)


def parse_spans(tokens, spans):
    for start, stop, type, weight in spans:
        start = tokens[start].start
        stop = tokens[stop - 1].stop
        yield Span(start, stop, type)


MITIE_STRIP = '\xa0\t\r\n '


def parse(text, data):
    chunks, spans = data
    tokens = list(find_tokens(chunks, text, strip=MITIE_STRIP))
    spans = list(parse_spans(tokens, spans))
    return MitieMarkup(text, spans)


def post(text, host, port):
    import requests

    url = MITIE_URL.format(
        host=host,
        port=port
    )
    payload = text.encode('utf8')
    response = requests.post(
        url,
        data=payload
    )
    response.raise_for_status()
    return response.json()


def call(text, host=MITIE_HOST, port=MITIE_PORT):
    data = post(text, host, port)
    return parse(text, data)


class MitieAnnotator(Annotator):
    name = MITIE
    host = MITIE_HOST
    port = MITIE_PORT

    def __call__(self, text):
        return call(text, self.host, self.port)


class MitieContainerAnnotator(MitieAnnotator, ContainerAnnotator):
    image = MITIE_IMAGE
    container_port = MITIE_CONTAINER_PORT


register(
    MITIE,
    MitieMarkup,
    MitieAnnotator,
    MitieContainerAnnotator
)
