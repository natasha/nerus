
import re
from functools import lru_cache

from .utils import Record


class Token(Record):
    __attributes__ = ['start', 'stop', 'text']

    def __init__(self, start, stop, text):
        self.start = start
        self.stop = stop
        self.text = text


def tokenize_(text):
    from razdel import tokenize as tokenize__

    for token in tokenize__(text):
        yield Token(
            token.start,
            token.stop,
            token.text
        )


@lru_cache(maxsize=10000)
def tokenize(text):
    return list(tokenize_(text))


CHUNK_ALIASES = {
    # for deeppavlov
    "''": '"',
    '``': '"',
    '"': "''",
}


def try_fix_chunk(chunk):
    if chunk in CHUNK_ALIASES:
        yield CHUNK_ALIASES[chunk]

    if chunk.startswith("'"):
        # for mitie
        #  `est -> ’est
        #  'est -> ’est
        #  's -> '’s
        #  'Рейли -> '’Рейли
        #  ' -> ’
        suffix = chunk[1:]
        yield '`' + suffix
        yield '’' + suffix


def try_skip_chunk(suffix):
    for skip in ['.']:
        if suffix.startswith(skip):
            return skip


def lstrip(text, chars=r'\s'):
    space = re.match(r'^([' + chars + ']*)', text).group(1)
    offset = len(space)
    return offset, text[offset:]


class FindTokenError(Exception):
    def __init__(self, chunk, chunks, text):
        self.chunk = chunk
        self.chunks = chunks
        self.text = text


def find_tokens(chunks, text, start=0, strip=r'\s'):
    offset, suffix = lstrip(text, strip)
    start += offset
    for index, chunk in enumerate(chunks):
        if suffix.startswith(chunk):
            size = len(chunk)
            stop = start + size
            yield Token(start, stop, chunk)
            offset, suffix = lstrip(suffix[size:], strip)
            start += size + offset
        else:
            skip = try_skip_chunk(suffix)
            if skip:
                try:
                    # recursion is practice is not deep
                    # for example [dr, li] 'dr....... li'
                    # is not the case
                    tokens = list(find_tokens(
                        chunks[index:],
                        suffix[len(skip):],
                        start=start,
                        strip=strip
                    ))
                except FindTokenError:
                    # in case need to try_fix_chunk instead
                    pass
                else:
                    yield from tokens
                    return

            for fix in try_fix_chunk(chunk):
                try:
                    tokens = list(find_tokens(
                        [fix] + chunks[index + 1:],
                        suffix,
                        start=start,
                        strip=strip
                    ))
                except FindTokenError:
                    # to try other fix
                    continue
                else:
                    yield from tokens
                    return

            raise FindTokenError(chunk, chunks, suffix)
