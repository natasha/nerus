
import requests

from nerus.const import (
    MITIE,
    MITIE_HOST,
    MITIE_PORT,

    MITIE_CONTAINER_PORT,
    MITIE_IMAGE,
    MITIE_URL,
)
from nerus.utils import Record
from nerus.token import find_tokens
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


class MitieMarkup(Record):
    __attributes__ = ['text', 'spans']
    label = MITIE

    def __init__(self, text, spans):
        self.text = text
        self.spans = spans

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield MitieMarkup(sent.text, list(spans))


def parse_spans(tokens, spans):
    for start, stop, type, weight in spans:
        start = tokens[start].start
        stop = tokens[stop - 1].stop
        yield Span(start, stop, type)


def parse(text, data):
    chunks, spans = data
    tokens = list(find_tokens(chunks, text))
    spans = list(parse_spans(tokens, spans))
    return MitieMarkup(text, spans)


##########
#
#   CALL
#
#########


def post(text):
    url = MITIE_URL.format(
        host=MITIE_HOST,
        port=MITIE_PORT
    )
    payload = text.encode('utf8')
    response = requests.post(
        url,
        data=payload
    )
    response.raise_for_status()
    return response.json()


def call(texts):
    for text in texts:
        data = post(text)
        yield parse(text, data)


###########
#
#   CONTAINER
#
#########


def start():
    start_container(
        MITIE_IMAGE,
        MITIE,
        MITIE_CONTAINER_PORT,
        MITIE_PORT
    )
    warmup_container(call)


def stop():
    stop_container(MITIE)
