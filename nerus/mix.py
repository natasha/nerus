
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
    else:
        [(first, first_count), (second, second_count)] = counts[:2]
        if first_count >= 2:
            if first_count == second_count:
                # 2 2 for examples, rare
                # assume tags ordered by annotator strength
                for tag in tags:
                    if tag == first or tag == second:
                        return tag
            else:
                return first
        else:
            return O


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
