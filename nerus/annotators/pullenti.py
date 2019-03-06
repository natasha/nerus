
from pullenti_client import Client as PullentiClient
from pullenti_client.result import (
    Span as PullentiSpan_,
    Match as PullentiMatch_,
    Result as PullentiMarkup_,
)
from pullenti_client.referent import (
    Slot as PullentiSlot_,
    Referent as PullentiReferent_
)

from nerus.const import (
    PULLENTI,
    PULLENTI_HOST,
    PULLENTI_PORT,

    PULLENTI_CONTAINER_PORT,
    PULLENTI_IMAGE,
)
from nerus.utils import (
    Record,
    parse_annotation
)
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


class PullentiRecord(Record):
    @classmethod
    def from_client(cls, record):
        args = []
        for key in cls.__attributes__:
            annotation = cls.__annotations__.get(key)
            type, repeatable, is_record = parse_annotation(annotation)
            value = getattr(record, key)
            if repeatable and is_record:
                value = [type.from_client(_) for _ in value]
            elif is_record:
                value = type.from_client(value)
            args.append(value)
        return cls(*args)


class PullentiSpan(PullentiSpan_, Span, PullentiRecord):
    def offset(self, delta):
        return PullentiSpan(
            self.start + delta,
            self.stop + delta
        )


class PullentiSlot(PullentiSlot_, PullentiRecord):
    # annotation is not supported
    #   value: (str, PullentiReferent)}

    @classmethod
    def from_client(cls, slot):
        value = slot.value
        if isinstance(value, PullentiReferent_):
            value = PullentiReferent.from_client(value)
        return PullentiSlot(
            slot.key,
            value
        )

    @classmethod
    def from_json(cls, data):
        key, value = [data[_] for _ in cls.__attributes__]
        if not isinstance(value, str):
            value = PullentiReferent.from_json(value)
        return cls(key, value)


class PullentiReferent(PullentiReferent_, PullentiRecord):
    __annotations__ = {
        'slots': [PullentiSlot]
    }


class PullentiMatch(PullentiMatch_, PullentiRecord):
    def offset(self, delta):
        return PullentiMatch(
            self.referent,
            self.span.offset(delta),
            [_.offset(delta) for _ in self.children]
        )

    @property
    def start(self):
        return self.span.start

    @property
    def stop(self):
        return self.span.stop

    @property
    def depth(self):
        if not self.children:
            return 1
        else:
            return 1 + max(_.depth for _ in self.children)


PullentiMatch.__annotations__ = {
    'referent': PullentiReferent,
    'span': PullentiSpan,
    'children': [PullentiMatch]
}


class PullentiMarkup(PullentiMarkup_, AnnotatorMarkup, PullentiRecord):
    __annotations__ = {
        'matches': [PullentiMatch]
    }

    label = PULLENTI

    @property
    def spans(self):
        for match in self.walk():
            start, stop = match.span
            yield Span(start, stop, match.referent.label)

    @property
    def sents(self):
        for sent in sentenize(self.text):
            matches = sent_spans(sent, self.matches)
            yield PullentiMarkup(sent.text, list(matches))

    @property
    def depth(self):
        if not self.matches:
            return
        return max(_.depth for _ in self.matches)


LOOP = PullentiReferent_('LOOP')


def remove_loops_(referent, visited):
    visited.add(id(referent))
    for slot in referent.slots:
        value = slot.value
        if isinstance(value, PullentiReferent_):
            if id(value) in visited:
                slot.value = LOOP
            else:
                remove_loops_(value, visited)


def remove_loops(result):
    for match in result.walk():
        visited = set()
        remove_loops_(match.referent, visited)


def map(texts, host=PULLENTI_HOST, port=PULLENTI_PORT):
    client = PullentiClient(host, port)
    for text in texts:
        result = client(text)
        # ~2% of docs, just ignore, maybe TODO
        remove_loops(result)
        yield PullentiMarkup.from_client(result)


class PullentiAnnotator(ChunkAnnotator):
    name = PULLENTI
    host = PULLENTI_HOST
    port = PULLENTI_PORT
    chunk = None

    def map(self, texts):
        return map(texts, self.host, self.port)


class PullentiContainerAnnotator(PullentiAnnotator, ContainerAnnotator):
    image = PULLENTI_IMAGE
    container_port = PULLENTI_CONTAINER_PORT
