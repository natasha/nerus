
import requests

from nerus.const import (
    TEXTERRA,
    TEXTERRA_HOST,
    TEXTERRA_PORT,
    TEXTERRA_CONTAINER_PORT,
    TEXTERRA_CHUNK,
    TEXTERRA_IMAGE,
    TEXTERRA_URL,
)
from nerus.utils import group_chunks
from nerus.span import Span
from nerus.sent import (
    sentenize,
    sent_spans
)

from .base import (
    AnnotatorMarkup,
    ChunkAnnotator,
    ContainerAnnotator
)


class TexterraMarkup(AnnotatorMarkup):
    label = TEXTERRA

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield TexterraMarkup(sent.text, list(spans))


def parse_annotations(data):
    if 'named-entity' not in data:
        return
    for item in data['named-entity']:
        start = item['start']
        stop = item['end']
        type = item['value']['tag']
        yield Span(start, stop, type)


def parse(data):
    for item in data:
        text = item['text']
        annotations = item['annotations']
        spans = list(parse_annotations(annotations))
        yield TexterraMarkup(text, spans)


def post(texts, host, port, timeout):
    url = TEXTERRA_URL.format(
        host=host,
        port=port
    )
    payload = [{'text': _} for _ in texts]
    response = requests.post(
        url,
        json=payload,
        timeout=timeout
    )
    response.raise_for_status()
    return response.json()


def map(texts, host=TEXTERRA_HOST, port=TEXTERRA_PORT, size=TEXTERRA_CHUNK, timeout=120):
    for chunk in group_chunks(texts, size):
        data = post(chunk, host, port, timeout)
        for markup in parse(data):
            yield markup


class TexterraAnnotator(ChunkAnnotator):
    name = TEXTERRA
    host = TEXTERRA_HOST
    port = TEXTERRA_PORT
    chunk = TEXTERRA_CHUNK

    def map(self, texts):
        return map(texts, self.host, self.port, self.chunk)


class TexterraContainerAnnotator(TexterraAnnotator, ContainerAnnotator):
    image = TEXTERRA_IMAGE
    container_port = TEXTERRA_CONTAINER_PORT