
from collections import OrderedDict
from itertools import islice

from .const import LABEL


def parse_annotation(annotation):
    type = annotation or str

    repeatable = False
    if isinstance(annotation, list):  # [Fact]
        repeatable = True
        type = annotation[0]

    is_record = issubclass(type, Record)

    return type, repeatable, is_record


class Record(object):
    __attributes__ = []
    __annotations__ = {}

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

    @property
    def as_json(self):
        data = OrderedDict()
        for key in self.__attributes__:
            annotation = self.__annotations__.get(key)
            _, repeatable, is_record = parse_annotation(annotation)

            value = getattr(self, key)
            if value is None:
                continue

            if repeatable and is_record:
                value = [_.as_json for _ in value]
            elif is_record:
                value = value.as_json

            data[key] = value
        return data

    @classmethod
    def from_json(cls, data):
        args = []
        for key in cls.__attributes__:
            annotation = cls.__annotations__.get(key)
            type, repeatable, is_record = parse_annotation(annotation)
            value = data.get(key)
            if value is None and repeatable:
                value = []
            elif value is not None:
                if repeatable and is_record:
                    value = [type.from_json(_) for _ in value]
                elif is_record:
                    value = type.from_json(value)
            args.append(value)
        return cls(*args)

    @property
    def as_bson(self):
        return self.as_json

    @classmethod
    def from_bson(cls, data):
        return cls.from_json(data)


class LabeledRecord(Record):
    label = None

    @staticmethod
    def find(self, label):
        raise NotImplementedError

    @classmethod
    def label_json(cls, data):
        data[LABEL] = cls.label
        # move label to front
        data.move_to_end(LABEL, last=False)
        return data

    @property
    def as_json(self):
        data = super(LabeledRecord, self).as_json
        return self.label_json(data)

    @classmethod
    def from_json(cls, data):
        if LABEL in data:
            label = data.pop(LABEL)
            Record = cls.find(label)
            return Record.from_json(data)
        else:
            return super(LabeledRecord, cls).from_json(data)


########
#
#   ZIP
#
#####


def strict_zip(*items):
    head = first(items)
    for item in items:
        if len(head) != len(item):
            raise ValueError('expected same size, head: {head}, item: {item}'.format(
                head=len(head),
                item=len(item)
            ))
    return zip(*items)


#######
#
#   ITER
#
#######


def first(items):
    return next(iter(items))


def head(items, count):
    return islice(items, count)


def skip(items, count):
    return islice(items, count, None)


def iter_len(items):
    return sum(1 for _ in items)


def iter_sents(items):
    for item in items:
        for sent in item.sents:
            yield sent


def iter_spans(items):
    for item in items:
        for span in item.spans:
            yield span


def read_iter(items, size):
    for _ in range(size):
        try:
            yield next(items)
        except StopIteration:
            break


def group_chunks(items, size):
    items = iter(items)
    group = list(read_iter(items, size))
    while group:
        yield group
        group = list(read_iter(items, size))


def group_weighted_chunks(items, size, measure):
    items = iter(items)
    chunk = []
    accumulator = 0
    for item in items:
        weight = measure(item)
        accumulator += weight
        if accumulator >= size and chunk:
            yield chunk
            chunk = []
            accumulator = weight
        chunk.append(item)
    if chunk:
        yield chunk
