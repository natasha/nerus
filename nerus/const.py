
from os import getenv

from .path import (
    get_dir,
    join_path,
    norm_path
)


LOCALHOST = 'localhost'


#######
#
#   MARKUP
#
########


PER = 'PER'
ORG = 'ORG'
LOC = 'LOC'


#######
#
#   BIO
#
######


B = 'B'
I = 'I'
O = 'O'


#######
#
#   FACTRU
#
########


FACTRU = 'factru'
FACTRU_URL = 'https://github.com/dialogue-evaluation/factRuEval-2016/archive/master.zip'
FACTRU_DIR = 'factRuEval-2016-master'
FACTRU_TESTSET = 'testset'
FACTRU_DEVSET = 'devset'


#######
#
#   NE5
#
#######


NE5 = 'ne5'
NE5_URL = 'http://www.labinform.ru/pub/named_entities/collection5.zip'
NE5_DIR = 'Collection5'


#######
#
#   LENTA
#
#######


LENTA = 'lenta'
LENTA_URL = 'https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.0/lenta-ru-news.csv.gz'
LENTA_FILENAME = 'lenta-ru-news.csv.gz'


##########
#
#  CORPORA
#
#########


CORPORA = [FACTRU, NE5, LENTA]

CORPORA_DIR = norm_path(join_path(get_dir(__file__), '..', 'data'))


########
#
#  ANNOTATORS
#
#######


ANNOTATORS_HOST = LOCALHOST
ANNOTATORS_BASE_PORT = 8080


#######
#
#   DEEPPAVLOV
#
########


DEEPPAVLOV = 'deeppavlov'
DEEPPAVLOV_HOST = getenv('DEEPPAVLOV_HOST', ANNOTATORS_HOST)
DEEPPAVLOV_PORT = int(getenv('DEEPPAVLOV_PORT', 8081))

DEEPPAVLOV_IMAGE = getenv('DEEPPAVLOV_IMAGE', 'natasha/deeppavlov-ner-ru')
DEEPPAVLOV_CONTAINER_PORT = 6004

DEEPPAVLOV_CHUNK = int(getenv('DEEPPAVLOV_CHUNK', 3))
DEEPPAVLOV_URL = 'http://{host}:{port}/answer'


#########
#
#  MITIE
#
#########


MITIE = 'mitie'
MITIE_HOST = getenv('MITIE_HOST', ANNOTATORS_HOST)
MITIE_PORT = int(getenv('MITIE_PORT', 8083))

MITIE_IMAGE = 'natasha/mitie-ner-ru'
MITIE_CONTAINER_PORT = 8080

MITIE_URL = 'http://{host}:{port}/'


#########
#
#   NATASHA
#
#########


NATASHA = 'natasha'
NATASHA_HOST = getenv('NATASHA_HOST', ANNOTATORS_HOST)
NATASHA_PORT = int(getenv('NATASHA_PORT', 8085))

NATASHA_IMAGE = 'natasha/natasha:0.10.0'
NATASHA_CONTAINER_PORT = 8080

NATASHA_URL = 'http://{host}:{port}/'


#######
#
#   PULLENTI
#
#####


PULLENTI = 'pullenti'
PULLENTI_HOST = getenv('PULLENTI_HOST', ANNOTATORS_HOST)
PULLENTI_PORT = int(getenv('PULLENTI_PORT', 8080))

PULLENTI_IMAGE = 'pullenti/pullenti-server'
PULLENTI_CONTAINER_PORT = 8080


########
#
#   TEXTERRA
#
###########


TEXTERRA = 'texterra'
TEXTERRA_HOST = getenv('TEXTERRA_HOST', ANNOTATORS_HOST)
TEXTERRA_PORT = int(getenv('TEXTERRA_PORT', 8082))

TEXTERRA_IMAGE = 'natasha/texterra-russian'
TEXTERRA_CONTAINER_PORT = 8080

TEXTERRA_CHUNK = 30
# if lang is undefined may try to load eng model and fail
TEXTERRA_URL = 'http://{host}:{port}/texterra/nlp?targetType=named-entity&language=ru'


#########
#
#  TOMITA
#
########


TOMITA = 'tomita'
TOMITA_HOST = getenv('TOMITA_HOST', ANNOTATORS_HOST)
TOMITA_PORT = int(getenv('TOMITA_PORT', 8084))

TOMITA_IMAGE = 'natasha/tomita-algfio'
TOMITA_CONTAINER_PORT = 8080

TOMITA_URL = 'http://{host}:{port}/'


########
#
#  ANNOTATORS
#
#########


ANNOTATORS = [DEEPPAVLOV, MITIE, NATASHA, PULLENTI, TEXTERRA, TOMITA]


##########
#
#   WORKER
#
#########


WORKER_ANNOTATOR = getenv('WORKER_ANNOTATOR', NATASHA)
WORKER_QUEUE = getenv('WORKER_QUEUE', NATASHA)


########
#
#   QUEUE
#
########


QUEUE_HOST = getenv('QUEUE_HOST', LOCALHOST)
QUEUE_PORT = int(getenv('QUEUE_PORT', 6379))
QUEUE_PASSWORD = getenv('QUEUE_PASSWORD', 'ENvHwwFLhiKe7hE')


########
#
#   DB
#
##########


CORPUS = 'corpus'
TEXT = 'text'
_ID = '_id'

DB_HOST = getenv('DB_HOST', LOCALHOST)
DB_PORT = int(getenv('DB_PORT', 27017))
DB_NAME = 'db'
DB_USERNAME = getenv('DB_USERNAME', 'root')
DB_PASSWORD = getenv('DB_PASSWORD', 'Yax6mUVzdXzsCCo')
