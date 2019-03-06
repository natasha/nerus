
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
from nerus.utils import Record
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


class PullentiSpan(PullentiSpan_, Span):
    def offset(self, delta):
        return PullentiSpan(
            self.start + delta,
            self.stop + delta
        )

    @classmethod
    def from_client(self, span):
        return PullentiSpan(
            span.start,
            span.stop
        )


class PullentiSlot(PullentiSlot_, Record):
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
        # since standart mechanism does not support loops
        # Referent -> Slot -> Referent
        key, value = [data[_] for _ in cls.__attributes__]
        if not isinstance(value, str):
            value = PullentiReferent.from_json(value)
        return cls(key, value)


class PullentiReferent(PullentiReferent_, Record):
    __annotations__ = {
        'slots': [PullentiSlot]
    }

    @classmethod
    def from_client(cls, referent):
        return PullentiReferent(
            referent.label,
            [PullentiSlot.from_client(_) for _ in referent.slots]
        )


class PullentiMatch(PullentiMatch_, Record):
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

    @classmethod
    def from_client(self, match):
        return PullentiMatch(
            PullentiReferent.from_client(match.referent),
            PullentiSpan.from_client(match.span),
            [PullentiMatch.from_client(_) for _ in match.children]
        )

    @classmethod
    def from_json(cls, data):
        # standart mechanism does not support recursion
        # match -> children
        referent, span, children = [data[_] for _ in cls.__attributes__]
        referent = PullentiReferent.from_json(referent)
        span = PullentiSpan.from_json(span)
        children = [PullentiMatch.from_json(_) for _ in children]
        return cls(referent, span, children)


class PullentiMarkup(PullentiMarkup_, AnnotatorMarkup):
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

    @classmethod
    def from_client(cls, result):
        return PullentiMarkup(
            result.text,
            [PullentiMatch.from_client(_) for _ in result.matches]
        )


def map(texts, host=PULLENTI_HOST, port=PULLENTI_PORT):
    client = PullentiClient(host, port)
    for text in texts:
        result = client(text)
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
