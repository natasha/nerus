
from .const import B, I, O
from .utils import strict_zip
from .span import (
    Span,
    assert_aligned_bounds,
    assert_non_overlapping,
    envelop_span,
)


def parse_bio(tag):
    if '-' in tag:
        part, type = tag.split('-', 1)
    else:
        part = tag
        type = None
    if part not in (B, I, O):
        raise ValueError(tag)
    return part, type


def format_bio(part, type):
    if part not in (B, I, O):
        raise ValueError(part)
    if not type:
        return part
    return part + '-' + type


def bio_spans(tokens, tags):
    previous = None
    start = None
    stop = None
    for token, tag in strict_zip(tokens, tags):
        part, type = parse_bio(tag)
        if part == O:
            if previous:
                yield Span(start, stop, previous)
                previous = None
        elif part == B:
            if previous:
                yield Span(start, stop, previous)
            previous = type
            start = token.start
            stop = token.stop
        elif part == I:
            stop = token.stop
    if previous:
        yield Span(start, stop, previous)


def spans_bio(tokens, spans, strict=True):
    if strict:
        assert_aligned_bounds(spans, tokens)
        assert_non_overlapping(spans)
    for token in tokens:
        part = O
        type = None
        for span in spans:
            if envelop_span(span, token):
                type = span.type
                if span.start == token.start:
                    part = B
                else:
                    part = I
                break
        yield format_bio(part, type)


def io_spans(tokens, tags):
    previous = None
    start = None
    stop = None
    for token, tag in strict_zip(tokens, tags):
        part, type = parse_bio(tag)
        # wikiner splits on I-PER B-PER for example
        if previous != type or part == B:
            if not previous and type:
                # O I
                start = token.start
            elif previous and type:
                # I-A I-B
                yield Span(start, stop, previous)
                start = token.start
            elif previous and not type:
                # I O
                yield Span(start, stop, previous)
                previous = None
        previous = type
        stop = token.stop
    if previous:
        yield Span(start, stop, previous)


def spans_io(tokens, spans, strict=True):
    if strict:
        assert_aligned_bounds(spans, tokens)
        assert_non_overlapping(spans)
    for token in tokens:
        part = O
        type = None
        for span in spans:
            if envelop_span(span, token):
                part = I
                type = span.type
                break
        yield format_bio(part, type)
