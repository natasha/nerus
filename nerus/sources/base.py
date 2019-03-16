
from nerus.utils import (
    Record,
    LabeledRecord
)


REGISTRY = {}


class RegistryRecord(Record):
    __attributes__ = ['Record', 'Source']

    def __init__(self, Record, Source):
        self.Record = Record
        self.Source = Source


def register(label, Record, Source):
    REGISTRY[label] = RegistryRecord(Record, Source)


class SourceRecord(LabeledRecord):
    __attributes__ = ['text']

    def __init__(self, text):
        self.text = text

    @property
    def sents(self):
        raise NotImplementedError

    @staticmethod
    def find(label):
        return REGISTRY[label].Record


class Source:
    name = None

    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def get():
        raise NotImplementedError

    @staticmethod
    def load():
        raise NotImplementedError

    @staticmethod
    def find(name):
        return REGISTRY[name].Source
