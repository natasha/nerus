
from corus import load_bsnlp as load_

from nerus.const import (
    BSNLP,
    BSNLP_DIR,
)

from nerus.sent import (
    sentenize,
    sent_spans
)
from nerus.markup import Markup
from nerus.span import Span
from nerus.adapt.bsnlp import adapt

from .base import (
    register,
    SourceRecord,
    Source
)


class BsnlpMarkup(Markup, SourceRecord):
    label = BSNLP

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield BsnlpMarkup(
                sent.text,
                list(spans)
            )

    @property
    def adapted(self):
        return adapt(self)

    @classmethod
    def from_corus(self, record):
        return BsnlpMarkup(
            record.text,
            [Span(_.start, _.stop, _.type) for _ in record.spans]
        )


def load(dir=BSNLP_DIR):
    for record in load_(dir):
        yield BsnlpMarkup.from_corus(record)


class BsnlpSource(Source):
    name = BSNLP
    load = staticmethod(load)


register(BSNLP, BsnlpMarkup, BsnlpSource)
