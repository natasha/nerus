

import pytest

from nerus.log import dot
from nerus.span import Span
from nerus.annotators.deeppavlov import (
    DeeppavlovMarkup,
    DeeppavlovContainerAnnotator
)
from nerus.annotators.mitie import (
    MitieMarkup,
    MitieContainerAnnotator
)
from nerus.annotators.natasha import (
    NatashaMarkup,
    NatashaMatch,
    NatashaContainerAnnotator
)
from nerus.annotators.pullenti import (
    PullentiMarkup,
    PullentiMatch,
    PullentiReferent,
    PullentiSlot,
    PullentiSpan,
    PullentiContainerAnnotator
)
from nerus.annotators.texterra import (
    TexterraMarkup,
    TexterraContainerAnnotator
)
from nerus.annotators.tomita import (
    TomitaMarkup,
    TomitaFact,
    TomitaContainerAnnotator
)


TEXTS = ['В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.']

TESTS = [
    [
        DeeppavlovContainerAnnotator,
        [DeeppavlovMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', spans=[Span(start=2, stop=5, type='LOC'), Span(start=38, stop=56, type='LOC'), Span(start=57, stop=75, type='PER'), Span(start=98, stop=104, type='LOC'), Span(start=137, stop=141, type='ORG')])]
    ],
    [
        MitieContainerAnnotator,
        [MitieMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', spans=[Span(start=2, stop=5, type='LOC'), Span(start=57, stop=75, type='PERS'), Span(start=98, stop=104, type='LOC'), Span(start=137, stop=141, type='ORG')])]
    ],
    [
        NatashaContainerAnnotator,
        [NatashaMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', matches=[NatashaMatch(start=2, stop=5, type='Location', fact={'name': 'сша'}), NatashaMatch(start=38, stop=75, type='Location', fact={'name': 'соединённый штат томас джефферсон'}), NatashaMatch(start=57, stop=75, type='Name', fact={'last': 'джефферсон', 'first': 'томас'})])]
    ],
    [
        PullentiContainerAnnotator,
        [PullentiMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', matches=[PullentiMatch(referent=PullentiReferent(label='GEO', slots=[PullentiSlot(key='ALPHA2', value='US'), PullentiSlot(key='NAME', value='США'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), PullentiSlot(key='TYPE', value='государство')]), span=PullentiSpan(start=2, stop=5), children=[]), PullentiMatch(referent=PullentiReferent(label='PERSON', slots=[PullentiSlot(key='SEX', value='MALE'), PullentiSlot(key='LASTNAME', value='ТОМАС'), PullentiSlot(key='FIRSTNAME', value='ДЖЕФФЕРСОН'), PullentiSlot(key='ATTRIBUTE', value=PullentiReferent(label='PERSONPROPERTY', slots=[PullentiSlot(key='REF', value=PullentiReferent(label='GEO', slots=[PullentiSlot(key='ALPHA2', value='US'), PullentiSlot(key='NAME', value='США'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), PullentiSlot(key='TYPE', value='государство')])), PullentiSlot(key='NAME', value='третий президент')]))]), span=PullentiSpan(start=18, stop=75), children=[PullentiMatch(referent=PullentiReferent(label='PERSONPROPERTY', slots=[PullentiSlot(key='REF', value=PullentiReferent(label='GEO', slots=[PullentiSlot(key='ALPHA2', value='US'), PullentiSlot(key='NAME', value='США'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), PullentiSlot(key='TYPE', value='государство')])), PullentiSlot(key='NAME', value='третий президент')]), span=PullentiSpan(start=18, stop=56), children=[PullentiMatch(referent=PullentiReferent(label='GEO', slots=[PullentiSlot(key='ALPHA2', value='US'), PullentiSlot(key='NAME', value='США'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), PullentiSlot(key='TYPE', value='государство')]), span=PullentiSpan(start=38, stop=56), children=[])])]), PullentiMatch(referent=PullentiReferent(label='GEO', slots=[PullentiSlot(key='TYPE', value='штат'), PullentiSlot(key='NAME', value='ТЕХАС')]), span=PullentiSpan(start=98, stop=104), children=[]), PullentiMatch(referent=PullentiReferent(label='ORGANIZATION', slots=[PullentiSlot(key='PROFILE', value='Media'), PullentiSlot(key='NAME', value='LIFE')]), span=PullentiSpan(start=137, stop=141), children=[])])]
    ],
    [
        TexterraContainerAnnotator,
        [TexterraMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', spans=[Span(start=2, stop=5, type='GPE_COUNTRY'), Span(start=38, stop=56, type='GPE_COUNTRY'), Span(start=57, stop=75, type='PERSON'), Span(start=98, stop=104, type='GPE_STATE_PROVINCE')])]
    ],
    [
        TomitaContainerAnnotator,
        [TomitaMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', facts=[TomitaFact(start=57, stop=75, first='ТОМАС', last='ДЖЕФФЕРСОН', middle=None, known_surname=False)])]
    ]
]


@pytest.mark.int
@pytest.mark.parametrize('constructor, etalon', TESTS)
def test_annotators(constructor, etalon):
    annotator = constructor()
    try:
        annotator.start()
        annotator.wait(dot)
        guess = list(annotator(TEXTS))
        assert guess == etalon
    except:
        raise
    finally:
        annotator.stop()
