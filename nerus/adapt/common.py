
from nerus.span import (
    select_type_spans,
    convert_span_types,
    filter_misaligned_spans,
)
from nerus.markup import Markup
from nerus.token import tokenize


QUOTES = '"\'”«„ʼ»“ʻ'
SPACES = ' \t'
DOT = '.'


def adapt_spans(spans, text, types):
    spans = select_type_spans(spans, types)
    spans = list(convert_span_types(spans, types))

    # ne5 typos is span.stop
    #   Magna Internationa -> Magna International
    #   Горсове -> Горсовет
    # tokenizer errors
    #   поезд Москва-Баку
    #   Yahoo!.
    tokens = list(tokenize(text))
    return filter_misaligned_spans(spans, tokens)


def adapt(markup, types):
    spans = list(adapt_spans(markup.spans, markup.text, types))
    return Markup(markup.text, spans)
