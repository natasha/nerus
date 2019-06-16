
from nerus.const import (
    NATASHA,
    NATASHA_HOST,
    NATASHA_PORT,
    NATASHA_CONTAINER_PORT,
    NATASHA_IMAGE,
    NATASHA_URL,
)
from nerus.span import Span
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.adapt.natasha import adapt

from .base import (
    register,
    AnnotatorMarkup,
    Annotator,
    ContainerAnnotator
)


class NatashaMatch(Span):
    __attributes__ = ['start', 'stop', 'type', 'fact']
    __annotations__ = {
        'start': int,
        'stop': int,
        'fact': dict
    }

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


class NatashaMarkup(AnnotatorMarkup):
    __attributes__ = ['text', 'matches']
    __annotations__ = {
        'matches': [NatashaMatch]
    }

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

    @property
    def adapted(self):
        return adapt(self)


def parse_matches(data):
    for item in data:
        type = item['type']
        fact = item['fact']
        start, stop = item['span']
        yield NatashaMatch(start, stop, type, fact)


def parse(text, data):
    matches = list(parse_matches(data))
    return NatashaMarkup(text, matches)


def post(text, host, port):
    import requests

    url = NATASHA_URL.format(
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


def call(text, host=NATASHA_HOST, port=NATASHA_PORT):
    data = post(text, host, port)
    return parse(text, data)


class NatashaAnnotator(Annotator):
    name = NATASHA
    host = NATASHA_HOST
    port = NATASHA_PORT

    def __call__(self, text):
        return call(text, self.host, self.port)


class NatashaContainerAnnotator(NatashaAnnotator, ContainerAnnotator):
    image = NATASHA_IMAGE
    container_port = NATASHA_CONTAINER_PORT


register(
    NATASHA,
    NatashaMarkup,
    NatashaAnnotator,
    NatashaContainerAnnotator
)
