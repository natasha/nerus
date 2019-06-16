
from nerus.const import (
    PER,

    TOMITA,
    TOMITA_HOST,
    TOMITA_PORT,

    TOMITA_CONTAINER_PORT,
    TOMITA_IMAGE,
    TOMITA_URL,
)
from nerus.etl import parse_xml
from nerus.span import Span
from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.adapt.tomita import adapt

from .base import (
    register,
    AnnotatorMarkup,
    Annotator,
    ContainerAnnotator
)


class TomitaFact(Span):
    __attributes__ = [
        'start', 'stop',
        'first', 'last', 'middle', 'known_surname'
    ]

    def __init__(self, start, stop,
                 first, last, middle, known_surname):
        self.start = start
        self.stop = stop
        self.first = first
        self.last = last
        self.middle = middle
        self.known_surname = known_surname

    def offset(self, delta):
        return TomitaFact(
            self.start + delta,
            self.stop + delta,
            self.first,
            self.last,
            self.middle,
            self.known_surname
        )


class TomitaMarkup(AnnotatorMarkup):
    __attributes__ = ['text', 'facts']
    __annotations__ = {
        'facts': [TomitaFact]
    }

    label = TOMITA

    def __init__(self, text, facts):
        self.text = text
        self.facts = facts

    @property
    def spans(self):
        for fact in self.facts:
            yield Span(fact.start, fact.stop, PER)

    @property
    def sents(self):
        for sent in sentenize(self.text):
            facts = sent_spans(sent, self.facts)
            yield TomitaMarkup(sent.text, list(facts))

    @property
    def adapted(self):
        return adapt(self)


def parse_facts(xml):
    if xml is None:
        return

    for item in xml.findall('Person'):
        start = int(item.get('pos'))
        size = int(item.get('len'))
        stop = start + size
        last = item.find('Name_Surname')
        if last is not None:
            last = last.get('val') or None
        first = item.find('Name_FirstName')
        if first is not None:
            first = first.get('val')
        middle = item.find('Name_Patronymic')
        if middle is not None:
            middle = middle.get('val')
        known_surname = item.find('Name_SurnameIsDictionary')
        if known_surname is not None:
            known_surname = int(known_surname.get('val'))
        known_surname = bool(known_surname)
        yield TomitaFact(
            start, stop,
            first, last, middle, known_surname
        )


def parse(text, xml):
    assert xml.tag == 'document', xml.tag
    facts = xml.find('facts')
    facts = list(parse_facts(facts))
    return TomitaMarkup(text, facts)


def call_(text, host, port):
    import requests

    url = TOMITA_URL.format(
        host=host,
        port=port
    )
    payload = text.encode('utf8')
    response = requests.post(
        url,
        data=payload
    )
    response.raise_for_status()
    return parse_xml(response.text)


def call(text, host=TOMITA_HOST, port=TOMITA_PORT):
    data = call_(text, host, port)
    return parse(text, data)


class TomitaAnnotator(Annotator):
    name = TOMITA
    host = TOMITA_HOST
    port = TOMITA_PORT

    def __call__(self, text):
        return call(text, self.host, self.port)


class TomitaContainerAnnotator(TomitaAnnotator, ContainerAnnotator):
    image = TOMITA_IMAGE
    container_port = TOMITA_CONTAINER_PORT


register(
    TOMITA,
    TomitaMarkup,
    TomitaAnnotator,
    TomitaContainerAnnotator
)
