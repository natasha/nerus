
from .etl import (
    load_gz_lines,
    parse_jsonl
)
from .span import Span
from .markup import Markup


def load_raw(path):
    from .dump import DumpRecord

    lines = load_gz_lines(path)
    records = parse_jsonl(lines)
    for record in records:
        yield DumpRecord.from_json(record)


########
#
#   NORM
#
#########


def parse_spans(items):
    for item in items:
        yield Span(
            item['span']['start'],
            item['span']['end'],
            item['type']
        )


def parse_norm(items):
    for item in items:
        yield Markup(
            item['content'],
            list(parse_spans(item['annotations']))
        )


def load_norm(path):
    lines = load_gz_lines(path)
    records = parse_jsonl(lines)
    return parse_norm(records)
