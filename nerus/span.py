
from collections import defaultdict

from .utils import Record


class Span(Record):
    __attributes__ = ['start', 'stop', 'type']
    __annotations__ = {
        'start': int,
        'stop': int
    }

    def __init__(self, start, stop, type=None):
        self.start = start
        self.stop = stop
        self.type = type

    def offset(self, delta):
        return Span(
            self.start + delta,
            self.stop + delta,
            self.type
        )


def offset_spans(spans, delta):
    for span in spans:
        yield span.offset(delta)


########
#
#   ENVELOP
#
##########


def envelop_span(envelope, span):
    return envelope.start <= span.start and span.stop <= envelope.stop


def envelop_spans(envelope, spans):
    for span in spans:
        if envelop_span(envelope, span):
            yield span


##########
#
#    ALIGN
#
############


def select_misaligned(envelopes, spans):
    starts = {_.start for _ in spans}
    stops = {_.stop for _ in spans}
    for span in envelopes:
        if span.start not in starts or span.stop not in stops:
            yield span


def filter_misaligned_spans(envelopes, spans):
    selected = select_misaligned(envelopes, spans)
    ids = {id(_) for _ in selected}
    for span in envelopes:
        if id(span) not in ids:
            yield span


def assert_aligned_bounds(envelopes, spans):
    for span in select_misaligned(envelopes, spans):
        raise ValueError('not aligned: %r' % span)


##########
#
#    OVERLAP
#
##########


def select_overlapping(spans):
    previous = None
    spans = sorted(spans, key=lambda _: (_.start, -_.stop))
    for span in spans:
        if previous and previous.stop > span.start:
            yield previous, span
            continue
        previous = span


def filter_overlapping(spans):
    ids = set()
    for previous, span in select_overlapping(spans):
        ids.add(id(span))
    for span in spans:
        if id(span) not in ids:
            yield span


def assert_non_overlapping(spans):
    for current, next in select_overlapping(spans):
        raise ValueError('%r overlap %r' % (current, next))


def split_overlapping_spans(spans):
    from intervaltree import IntervalTree as Intervals

    order = {}
    for index, span in enumerate(spans):
        order[id(span)] = index

    intervals = Intervals()
    for span in spans:
        intervals.addi(span.start, span.stop, span)

    intervals.split_overlaps()

    groups = defaultdict(list)
    for start, stop, span in intervals:
        groups[start, stop].append(span)

    for start, stop in sorted(groups):
        spans = groups[start, stop]
        spans = sorted(spans, key=lambda _: order[id(_)])
        type = spans[-1].type
        yield Span(start, stop, type)


########
#
#   TYPE
#
##########


def select_type_spans(spans, types):
    for span in spans:
        if span.type in types:
            yield span


def convert_span_types(spans, types):
    for span in spans:
        type = span.type
        if type not in types:
            raise KeyError('missing: %r, types: %r' % (type, sorted(types)))
        yield Span(
            span.start,
            span.stop,
            types[type]
        )


###########
#
#   STRIP
#
#########


def strip_span(span, text, chars):
    chunk = text[span.start:span.stop]
    word = chunk.strip(chars)
    size = len(word)
    offset = chunk.find(word)
    start = span.start + offset
    stop = start + size
    return Span(start, stop, span.type)


def strip_spans(spans, text, chars):
    for span in spans:
        yield strip_span(span, text, chars)


def filter_empty_spans(spans):
    for span in spans:
        if span.start != span.stop:
            yield span
