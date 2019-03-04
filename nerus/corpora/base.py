
from nerus.utils import Record


class CorpusRecord(Record):
    __attributes__ = ['text']

    @property
    def sents(self):
        raise NotImplementedError


class CorpusSchema:
    name = None
    get = None
    load = None
