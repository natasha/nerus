
try:
    from pullenti_client.result import (
        Span as PullentiSpan_,
        Match as PullentiMatch_,
        Result as PullentiMarkup_,
    )
except ImportError:
    class PullentiObject:
        def __init__(self, *args, **kwargs):
            raise ImportError('pullenti')

    PullentiSpan_ = PullentiObject
    PullentiMatch_ = PullentiObject
    PullentiMarkup_ = PullentiObject


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
from nerus.adapt.pullenti import adapt

from .base import (
    register,
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
    def from_client(cls, span):
        return PullentiSpan(span.start, span.stop)


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
    def from_client(cls, match):
        return PullentiMatch(
            match.referent,
            PullentiSpan.from_client(match.span),
            [PullentiMatch.from_client(_) for _ in match.children]
        )


class PullentiMarkup(PullentiMarkup_, AnnotatorMarkup):
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
    def adapted(self):
        return adapt(self)

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

    @property
    def as_json(self):
        data = PullentiMarkup_.as_json.fget(self)
        return self.label_json(data)

    @classmethod
    def from_json(cls, data):
        result = PullentiMarkup_.from_json(data)
        return cls.from_client(result)


def map(texts, host=PULLENTI_HOST, port=PULLENTI_PORT):
    from pullenti_client import Client as PullentiClient

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


register(
    PULLENTI,
    PullentiMarkup,
    PullentiAnnotator,
    PullentiContainerAnnotator
)
