
from collections import Counter

from .const import O
from .bio import (
    io_spans,
    spans_io
)
from .token import tokenize
from .markup import Markup


def choose_tag(tags):
    tags = [_ for _ in tags if _ != O]
    if not tags:
        return O
    counts = Counter(tags).most_common()
    if len(counts) == 1:
        tag, count = counts[0]
        if count >= 2:
            return tag
        else:
            return O
    else:  # >= 2
        [(first, first_count), (second, second_count)] = counts[:2]
        # TODO what about 2 2
        if first_count >= 2:
            return first
        else:
            # first = 1, second = 1
            # assume models ordered by strength
            return tags[0]


def mix(multi):
    tokens = list(tokenize(multi.text))
    tags = (
        spans_io(tokens, _.spans)
        for _ in multi.markups
        if _.text == multi.text  # super rare deeppavlov != multi.text
    )
    tags = zip(*tags)
    tags = [choose_tag(_) for _ in tags]
    spans = io_spans(tokens, tags)
    return Markup(multi.text, list(spans))
