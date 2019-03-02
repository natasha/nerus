
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
from nerus.utils import (
    Record,
    group_chunks
)
from nerus.span import Span
from nerus.sent import (
    sentenize,
    sent_spans
)

from .docker import (
    start_container,
    stop_container,
    warmup_container
)


class TexterraMarkup(Record):
    __attributes__ = ['text', 'spans']
    label = TEXTERRA

    def __init__(self, text, spans):
        self.text = text
        self.spans = spans

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


def post(texts, timeout):
    url = TEXTERRA_URL.format(
        host=TEXTERRA_HOST,
        port=TEXTERRA_PORT
    )
    payload = [{'text': _} for _ in texts]
    response = requests.post(
        url,
        json=payload,
        timeout=timeout
    )
    response.raise_for_status()
    return response.json()


#########
#
#    CALL
#
######


def call(texts, size=TEXTERRA_CHUNK, timeout=120):
    for chunk in group_chunks(texts, size):
        data = post(chunk, timeout)
        for markup in parse(data):
            yield markup


########
#
#   CONTAINER
#
#########


def warmup_call(texts):
    return call(texts, size=1, timeout=10)


def warmup():
    warmup_container(
        warmup_call,
        retries=20,
        delay=5
    )


def start():
    start_container(
        TEXTERRA_IMAGE,
        TEXTERRA,
        TEXTERRA_CONTAINER_PORT,
        TEXTERRA_PORT
    )
    warmup()


def stop():
    stop_container(TEXTERRA)
