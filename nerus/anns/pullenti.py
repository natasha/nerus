
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


class PullentiSpan(PullentiSpan_):
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


class PullentiMatch(PullentiMatch_):
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


class PullentiMarkup(PullentiMarkup_):
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


class PullentiSlot(PullentiSlot_):
    @classmethod
    def from_client(cls, slot):
        value = slot.value
        if isinstance(value, PullentiReferent_):
            value = PullentiReferent.from_client(value)
        return PullentiSlot(
            slot.key,
            value
        )


class PullentiReferent(PullentiReferent_):
    @classmethod
    def from_client(cls, referent):
        return PullentiReferent(
            referent.label,
            [PullentiSlot.from_client(_) for _ in referent.slots]
        )


#########
#
#   CALL
#
#########


def call(texts):
    client = PullentiClient(PULLENTI_HOST, PULLENTI_PORT)
    for text in texts:
        result = client(text)
        yield PullentiMarkup.from_client(result)


########
#
#   CONTAINER
#
##########


def warmup():
    warmup_container(call)


def start():
    start_container(
        PULLENTI_IMAGE,
        PULLENTI,
        PULLENTI_CONTAINER_PORT,
        PULLENTI_PORT
    )
    warmup()


def stop():
    stop_container(PULLENTI)
