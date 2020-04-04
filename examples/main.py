
import sys
from os.path import (
    expanduser,
    join as join_path
)
from itertools import islice as head
from contextlib import contextmanager

from ipymarkup import (
    format_dep_ascii_markup,
    show_span_ascii_markup
)

from naeval.io import (
    load_gz_lines,
    parse_jl
)
from naeval.record import from_jsons
from naeval.segment.partition import (
    parse_partitions,
    show_partition
)
from naeval.morph.markup import (
    Markup as MorphMarkup,
    show_markup_diff as show_morph_markup_diff
)
from naeval.syntax.markup import (
    Markup as SyntaxMarkup,
    token_deps
)
from naeval.ner.markup import Markup as NERMarkup

from nerus import load_nerus


NAEVAL_DATA = expanduser('~/proj/naeval/data')

NAEVAL_TOKEN_TARGET = join_path(NAEVAL_DATA, 'segment/token/dataset/syntag.jl.gz')
NAEVAL_TOKEN_PRED = join_path(NAEVAL_DATA, 'segment/token/razdel/syntag.jl.gz')

NAEVAL_MORPH_TARGET = join_path(NAEVAL_DATA, 'morph/dataset/news.jl.gz')
NAEVAL_MORPH_PRED = join_path(NAEVAL_DATA, 'morph/slovnet_bert/news.jl.gz')

NAEVAL_SYNTAX_TARGET = join_path(NAEVAL_DATA, 'syntax/dataset/news.jl.gz')
NAEVAL_SYNTAX_PRED = join_path(NAEVAL_DATA, 'syntax/slovnet_bert/news.jl.gz')

NAEVAL_NER_TARGET = join_path(NAEVAL_DATA, 'ner/dataset/ne5.jl.gz')
NAEVAL_NER_PRED = join_path(NAEVAL_DATA, 'ner/slovnet_bert/ne5.jl.gz')

NERUS = expanduser('~/proj/nerus/scripts/data/nerus_lenta.conllu.gz')

SAMPLE_DIR = 'sample'
SAMPLE_MORPH = join_path(SAMPLE_DIR, 'morph.txt')
SAMPLE_SYNTAX = join_path(SAMPLE_DIR, 'syntax.txt')
SAMPLE_NER = join_path(SAMPLE_DIR, 'ner.txt')


def format_syntax_markup(markup):
    deps = token_deps(markup.tokens)
    return format_dep_ascii_markup(markup.words, deps)


def format_syntax_markup_diff(a, b):
    a = list(format_syntax_markup(a))
    size = max(len(_) for _ in a)

    b = format_syntax_markup(b)
    for a, b in zip(a, b):
        sep = ' ' if a == b else '|'
        a = a.ljust(size)
        yield f'{a} {sep} {b}'


def show_syntax_markup_diff(a, b):
    for line in format_syntax_markup_diff(a, b):
        print(line)


def show_ner_markup(markup):
    show_span_ascii_markup(markup.text, markup.spans)


def iter_sents(records):
    for record in records:
        for sent in record.sents:
            yield sent


@contextmanager
def capture(path):
    standart = sys.stdout
    file = open(path, 'w')
    sys.stdout = file
    yield
    file.close()
    sys.stdout = standart
