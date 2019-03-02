

import requests

from nerus.const import (
    NATASHA,
    NATASHA_HOST,
    NATASHA_PORT,
    NATASHA_CONTAINER_PORT,
    NATASHA_IMAGE,
    NATASHA_URL,
)
from nerus.utils import Record
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


class NatashaMarkup(Record):
    __attributes__ = ['text', 'matches']
    label = NATASHA

    def __init__(self, text, matches):
        self.text = text
        self.matches = matches

    @property
    def spans(self):
        for match in self.matches:
            yield Span(match.start, match.stop, match.type)

    @property
    def sents(self):
        for sent in sentenize(self.text):
            matches = sent_spans(sent, self.matches)
            yield NatashaMarkup(sent.text, list(matches))


class NatashaMatch(Record):
    __attributes__ = ['start', 'stop', 'type', 'fact']

    def __init__(self, start, stop, type, fact):
        self.start = start
        self.stop = stop
        self.type = type
        self.fact = fact

    def offset(self, delta):
        return NatashaMatch(
            self.start + delta,
            self.stop + delta,
            self.type,
            self.fact
        )


def parse_matches(data):
    for item in data:
        type = item['type']
        fact = item['fact']
        start, stop = item['span']
        yield NatashaMatch(start, stop, type, fact)


def parse(text, data):
    matches = list(parse_matches(data))
    return NatashaMarkup(text, matches)


#########
#
#   CALL
#
########


def post(text):
    url = NATASHA_URL.format(
        host=NATASHA_HOST,
        port=NATASHA_PORT
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


#########
#
#   CONTAINER
#
#########


def warmup():
    warmup_container(call)


def start():
    start_container(
        NATASHA_IMAGE,
        NATASHA,
        NATASHA_CONTAINER_PORT,
        NATASHA_PORT
    )
    warmup()


def stop():
    stop_container(NATASHA)
