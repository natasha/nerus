
from nerus.span import (
    select_type_spans,
    convert_span_types,
    strip_spans,
    filter_misaligned_spans,
    filter_overlapping,
    filter_empty_spans,
    split_overlapping_spans,
)
from nerus.markup import Markup
from nerus.token import tokenize


QUOTES = '"\'”«„ʼ»“ʻ'
SPACES = ' \t'


def adapt_spans(spans, text, types):
    spans = select_type_spans(spans, types)
    spans = convert_span_types(spans, types)

    # in mitie and sometimes in deeppavlov
    spans = list(strip_spans(spans, text, QUOTES))

    # ne5 typos is span.stop
    #   Magna Internationa -> Magna International
    #   Горсове -> Горсовет
    # tokenizer errors
    #   поезд Москва-Баку
    #   Yahoo!.
    tokens = list(tokenize(text))
    spans = list(filter_misaligned_spans(spans, tokens))

    # ne5 bug
    #   Бражский район Подмосковья
    #   --------------
    #            -----------------
    spans = list(filter_overlapping(spans))

    return spans


def adapt_overlapping_spans(spans, text):
    spans = split_overlapping_spans(spans)
    spans = strip_spans(spans, text, SPACES)
    return filter_empty_spans(spans)


def adapt(markup, types):
    spans = adapt_spans(list(markup.spans), markup.text, types)
    return Markup(markup.text, list(spans))
