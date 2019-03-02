
from collections import OrderedDict


class Record(object):
    __attributes__ = []

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
            value = getattr(self, key)
            if value is None:
                continue
            if isinstance(value, Record):
                value = value.as_json
            elif isinstance(value, list):
                value = [_.as_json for _ in value]
            data[key] = value
        return data


########
#
#   ZIP
#
#####


def strict_zip(*items):
    head = first(items)
    for item in items:
        if len(head) != len(item):
            raise ValueError('expected same size, first: {head}, item: {item}'.format(
                head=len(head),
                item=len(item)
            ))
    return zip(*items)


def transpose(items):
    return strict_zip(*items)


#######
#
#   ITER
#
#######


def first(items):
    return next(iter(items))


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
