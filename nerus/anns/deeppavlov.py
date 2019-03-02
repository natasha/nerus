
import requests

from nerus.const import (
    DEEPPAVLOV,
    DEEPPAVLOV_HOST,
    DEEPPAVLOV_PORT,
    DEEPPAVLOV_CHUNK,

    DEEPPAVLOV_CONTAINER_PORT,
    DEEPPAVLOV_IMAGE,
    DEEPPAVLOV_URL,
)
from nerus.utils import (
    Record,
    strict_zip,
    group_chunks
)
from nerus.token import find_tokens
from nerus.bio import bio_spans
from nerus.sent import (
    sentenize,
    sent_spans
)

from .docker import (
    start_container,
    stop_container,
    warmup_container
)


class DeeppavlovMarkup(Record):
    __attributes__ = ['text', 'spans']
    label = DEEPPAVLOV

    def __init__(self, text, spans):
        self.text = text
        self.spans = spans

    @property
    def sents(self):
        for sent in sentenize(self.text):
            spans = sent_spans(sent, self.spans)
            yield DeeppavlovMarkup(
                sent.text,
                list(spans)
            )


def parse(texts, data):
    for text, (chunks, tags) in strict_zip(texts, data):
        tokens = list(find_tokens(chunks, text))
        spans = list(bio_spans(tokens, tags))
        yield DeeppavlovMarkup(text, spans)


###########
#
#    CALL
#
#########


def post(texts):
    url = DEEPPAVLOV_URL.format(
        host=DEEPPAVLOV_HOST,
        port=DEEPPAVLOV_PORT
    )
    payload = {'text1': texts}
    response = requests.post(
        url,
        json=payload
    )
    response.raise_for_status()
    return response.json()


def call(texts, size=DEEPPAVLOV_CHUNK):
    for chunk in group_chunks(texts, size):
        data = post(chunk)
        for markup in parse(chunk, data):
            yield markup


##########
#
#   CONTAINER
#
#############


def warmup():
    warmup_container(
        call,
        retries=15,
        delay=10
    )


def start():
    start_container(
        DEEPPAVLOV_IMAGE,
        DEEPPAVLOV,
        DEEPPAVLOV_CONTAINER_PORT,
        DEEPPAVLOV_PORT
    )
    warmup()


def stop():
    stop_container(DEEPPAVLOV)
