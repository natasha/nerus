
import re
import gzip
from itertools import groupby


#######
#
#  IO
#
#######


def load_gz_lines(path, encoding='utf8'):
    with gzip.open(path) as file:
        for line in file:
            yield line.decode(encoding).rstrip()


######
#
#   RECORD
#
######


class Record(object):
    __attributes__ = []

    def __init__(self, *args):
        for key, value in zip(self.__attributes__, args):
            self.__dict__[key] = value

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and all(
                (getattr(self, _) == getattr(other, _))
                for _ in self.__attributes__
            )
        )

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return (getattr(self, _) for _ in self.__attributes__)

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        name = self.__class__.__name__
        args = ', '.join(
            '{key}={value!r}'.format(
                key=_,
                value=getattr(self, _)
            )
            for _ in self.__attributes__
        )
        return '{name}({args})'.format(
            name=name,
            args=args
        )

    def _repr_pretty_(self, printer, cycle):
        name = self.__class__.__name__
        if cycle:
            printer.text('{name}(...)'.format(name=name))
        else:
            printer.text('{name}('.format(name=name))
            keys = self.__attributes__
            size = len(keys)
            if size:
                with printer.indent(4):
                    printer.break_()
                    for index, key in enumerate(keys):
                        printer.text(key + '=')
                        value = getattr(self, key)
                        printer.pretty(value)
                        if index < size - 1:
                            printer.text(',')
                            printer.break_()
                printer.break_()
            printer.text(')')


#######
#
#   SPAN
#
######


class Span(Record):
    __attributes__ = ['start', 'stop', 'type']

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


#######
#
#   TOKEN
#
#######


class Token(Record):
    __attributes__ = ['start', 'stop', 'text']


def find_tokens(text, chunks):
    offset = 0
    for chunk in chunks:
        start = text.find(chunk, offset)
        stop = start + len(chunk)
        yield Token(start, stop, chunk)
        offset = stop


#######
#
#   BIO
#
########


B, I, O = 'BIO'


def parse_bio(tag):
    if '-' in tag:
        part, type = tag.split('-', 1)
    else:
        part = tag
        type = None
    return part, type


def bio_spans(tokens, tags):
    previous = None
    start = None
    stop = None
    for token, tag in zip(tokens, tags):
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


#######
#
#  MARKUP
#
#####


class NERMarkup(Record):
    __attributes__ = ['text', 'spans']

    def show(self):
        return show_ner_markup(self)


class MorphToken(Record):
    __attributes__ = ['text', 'pos', 'feats']


class MorphMarkup(Record):
    __attributes__ = ['tokens']

    def show(self):
        return show_morph_markup(self)


class SyntaxToken(Record):
    __attributes__ = ['id', 'text', 'head_id', 'rel']


class SyntaxMarkup(Record):
    __attributes__ = ['tokens']

    def show(self):
        return show_syntax_markup(self)


def show_ner_markup(markup):
    try:
        from ipymarkup import show_span_ascii_markup
    except ImportError:
        raise ImportError('install ipymarkup')

    show_span_ascii_markup(markup.text, markup.spans)


def format_morph_tag(pos, feats):
    if not feats:
        return pos

    feats = '|'.join(
        '%s=%s' % (_, feats[_])
        for _ in sorted(feats)
    )
    return '%s|%s' % (pos, feats)


def format_morph_markup(markup, size=20):
    words, tags = [], []
    for token in markup.tokens:
        words.append(token.text)
        tags.append(format_morph_tag(token.pos, token.feats))

    for word, tag in zip(words, tags):
        word = word.rjust(size)
        yield '%s  %s' % (word, tag)


def show_morph_markup(markup):
    for line in format_morph_markup(markup):
        print(line)


def conll_deps(tokens):
    for token in tokens:
        id = int(token.id)
        head_id = int(token.head_id)
        rel = token.rel
        id = id - 1
        if head_id == 0:  # skip root=0
            continue
        head_id = head_id - 1
        yield head_id, id, rel


def show_syntax_markup(markup):
    try:
        from ipymarkup import show_dep_ascii_markup
    except ImportError:
        raise ImportError('install ipymarkup')

    words = [_.text for _ in markup.tokens]
    deps = list(conll_deps(markup.tokens))
    show_dep_ascii_markup(words, deps)


#####
#
#  NERUS
#
########

# # newdoc id = 0
# # sent_id = 0_0
# # text = Вице-премьер по социальным вопросам Татьяна Голикова рассказала, ...
# 1       Вице-премьер    _       NOUN    _       Anma=A   7       nsubj   _       Tag=O
# 2       по      _       ADP     _       _       4       case    _       Tag=O
# ...


class NerusToken(Record):
    __attributes__ = ['id', 'text', 'pos', 'feats', 'head_id', 'rel', 'tag']

    @property
    def morph(self):
        return MorphToken(self.text, self.pos, self.feats)

    @property
    def syntax(self):
        return SyntaxToken(self.id, self.text, self.head_id, self.rel)


class NerusSent(Record):
    __attributes__ = ['id', 'text', 'tokens']

    @property
    def ner(self):
        spans = list(sent_spans(self))
        return NERMarkup(self.text, spans)

    @property
    def morph(self):
        tokens = [_.morph for _ in self.tokens]
        return MorphMarkup(tokens)

    @property
    def syntax(self):
        tokens = [_.syntax for _ in self.tokens]
        return SyntaxMarkup(tokens)


class NerusDoc(Record):
    __attributes__ = ['id', 'sents']

    @property
    def ner(self):
        return join_ner_markups(_.ner for _ in self.sents)


def sent_spans(sent):
    words, tags = [], []
    for token in sent.tokens:
        words.append(token.text)
        tags.append(token.tag)

    tokens = find_tokens(sent.text, words)
    return bio_spans(tokens, tags)


def join_ner_markups(markups, sep=' '):
    texts, spans = [], []
    offset = 0
    for markup in markups:
        texts.append(markup.text)
        spans.extend(offset_spans(markup.spans, offset))
        offset += len(markup.text) + len(sep)
    return NERMarkup(sep.join(texts), spans)


def parse_feats(feats):
    if not feats:
        return

    for pair in feats.split('|'):
        key, value = pair.split('=', 1)
        yield key, value


def parse_tag(tag):
    # Tag=O
    return tag[4:]


def _none(value):
    if value == '_':
        return
    return value


def parse_row(line):
    return [_none(_) for _ in line.split('\t')]


def parse_token(line):
    id, text, _, pos, _, feats, head_id, rel, _, tag = parse_row(line)
    feats = dict(parse_feats(feats))
    tag = parse_tag(tag)
    return NerusToken(id, text, pos, feats, head_id, rel, tag)


def group_sents(lines):
    buffer = []
    for line in lines:
        if not line:
            yield buffer
            buffer = []
        else:
            buffer.append(line)
    if buffer:
        yield buffer


def parse_attr(line):
    line = line.lstrip('# ')
    return line.split(' = ', 1)


def parse_sents(lines):
    for group in group_sents(lines):
        attrs = {}
        tokens = []
        for line in group:
            if line.startswith('#'):
                key, value = parse_attr(line)
                attrs[key] = value
            else:
                token = parse_token(line)
                tokens.append(token)

        id = attrs['sent_id']
        text = attrs['text']

        yield NerusSent(id, text, tokens)


def doc_id(sent):
    match = re.match(r'^(\d+)_\d+$', sent.id)
    return match.group(1)


def group_docs(sents):
    for id, group in groupby(sents, key=doc_id):
        yield NerusDoc(id, list(group))


def parse_nerus(lines):
    sents = parse_sents(lines)
    return group_docs(sents)


def load_nerus(path):
    lines = load_gz_lines(path)
    return parse_nerus(lines)
