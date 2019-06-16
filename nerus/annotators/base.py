
from time import sleep

from nerus.utils import (
    Record,
    LabeledRecord
)
from nerus.const import (
    LOCALHOST,
    ANNOTATORS_BASE_PORT
)
from nerus.markup import Markup
from nerus.docker import (
    start_container,
    remove_container,
    generate_name,
    generate_port
)


REGISTRY = {}


class RegistryRecord(Record):
    __attributes__ = ['Markup', 'Annotator', 'ContainerAnnotator']

    def __init__(self, Markup, Annotator, ContainerAnnotator):
        self.Markup = Markup
        self.Annotator = Annotator
        self.ContainerAnnotator = ContainerAnnotator


def register(label, Markup, Annotator, ContainerAnnotator):
    REGISTRY[label] = RegistryRecord(Markup, Annotator, ContainerAnnotator)


class AnnotatorError(Exception):
    pass


class AnnotatorMarkup(Markup, LabeledRecord):
    @staticmethod
    def find(label):
        return REGISTRY[label].Markup


PUTIN = 'Путин'


class Annotator(Record):
    __attributes__ = ['host', 'port']

    name = None

    def __init__(self, host=None, port=None):
        if not host:
            host = self.host
        self.host = host
        if not port:
            port = self.port
        self.port = port

    def __call__(self, text):
        raise NotImplementedError

    def map(self, texts):
        for text in texts:
            yield self(text)

    @property
    def ready(self):
        from requests import RequestException

        try:
            self(PUTIN)
            return True
        except (RequestException, AnnotatorError):
            return False

    def wait(self, callback=None, retries=30, delay=2):
        for _ in range(retries):
            if self.ready:
                break
            else:
                if callback:
                    callback()
                sleep(delay)
        else:
            raise AnnotatorError('failed to start')

    @staticmethod
    def find(name):
        return REGISTRY[name].Annotator


class ChunkAnnotator(Annotator):
    __attributes__ = ['host', 'port', 'chunk']

    def map(self, texts):
        raise NotImplementedError

    def __call__(self, text):
        return next(self.map([text]))


class ContainerAnnotator(Annotator):
    image = None
    container_port = None

    def __init__(self):
        super(ContainerAnnotator, self).__init__(LOCALHOST, port=None)
        self.container_name = None

    def __call__(self, texts):
        if not self.port:
            raise AnnotatorError('container not running')
        return super(ContainerAnnotator, self).__call__(texts)

    def start(self):
        self.container_name = generate_name(prefix=self.name)
        self.port = generate_port(start=ANNOTATORS_BASE_PORT)
        start_container(
            self.image,
            self.container_name,
            self.container_port,
            self.port
        )

    def stop(self):
        remove_container(self.container_name)
        self.container_name = None
        self.port = None
