

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
FACTRU_DIR = 'factRuEval-2016-master'
FACTRU_TESTSET = 'testset'
FACTRU_DEVSET = 'devset'


#######
#
#   NE5
#
#######


NE5 = 'ne5'
NE5_DIR = 'Collection5'


########
#
#  ZOO
#
#########


ZOO_HOST = 'localhost'
WARMUP_TEXTS = ['Путин']


#######
#
#   DEEPPAVLOV
#
########


DEEPPAVLOV = 'deeppavlov'

DEEPPAVLOV_HOST = ZOO_HOST
DEEPPAVLOV_PORT = 8081

DEEPPAVLOV_IMAGE = 'natasha/deeppavlov-ner-ru'
DEEPPAVLOV_CONTAINER_PORT = 6004

DEEPPAVLOV_CHUNK = 3
DEEPPAVLOV_URL = 'http://{host}:{port}/answer'


#########
#
#  MITIE
#
#########


MITIE = 'mitie'

MITIE_HOST = ZOO_HOST
MITIE_PORT = 8083

MITIE_IMAGE = 'natasha/mitie-ner-ru'
MITIE_CONTAINER_PORT = 8080

MITIE_URL = 'http://{host}:{port}/'


#########
#
#   NATASHA
#
#########


NATASHA = 'natasha'

NATASHA_HOST = ZOO_HOST
NATASHA_PORT = 8085

NATASHA_IMAGE = 'natasha/natasha:0.10.0'
NATASHA_CONTAINER_PORT = 8080

NATASHA_URL = 'http://{host}:{port}/'


#######
#
#   PULLENTI
#
#####


PULLENTI = 'pullenti'

PULLENTI_HOST = ZOO_HOST
PULLENTI_PORT = 8080

PULLENTI_IMAGE = 'pullenti/pullenti-server'
PULLENTI_CONTAINER_PORT = 8080


########
#
#   TEXTERRA
#
###########


TEXTERRA = 'texterra'

TEXTERRA_HOST = ZOO_HOST
TEXTERRA_PORT = 8082

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

TOMITA_HOST = ZOO_HOST
TOMITA_PORT = 8084

TOMITA_IMAGE = 'natasha/tomita-algfio'
TOMITA_CONTAINER_PORT = 8080

TOMITA_URL = 'http://{host}:{port}/'
