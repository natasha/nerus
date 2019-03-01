

import pytest

from nerus.zoo import (
    deeppavlov,
    mitie,
    natasha,
    pullenti,
    texterra,
    tomita
)
from nerus.span import Span
from nerus.zoo.deeppavlov import DeeppavlovMarkup
from nerus.zoo.mitie import MitieMarkup
from nerus.zoo.natasha import (
    NatashaMarkup,
    NatashaMatch
)
from nerus.zoo.pullenti import (
    PullentiMarkup,
    PullentiMatch,
    PullentiSpan
)
from pullenti_client.referent import (
    Referent,
    Slot
)
from nerus.zoo.texterra import TexterraMarkup
from nerus.zoo.tomita import (
    TomitaMarkup,
    TomitaFact
)


TEXTS = ['В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.']

TESTS = [
    [
        deeppavlov,
        [DeeppavlovMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', spans=[Span(start=2, stop=5, type='LOC'), Span(start=38, stop=56, type='LOC'), Span(start=57, stop=75, type='PER'), Span(start=98, stop=104, type='LOC'), Span(start=137, stop=141, type='ORG')])]
    ],
    [
        mitie,
        [MitieMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', spans=[Span(start=2, stop=5, type='LOC'), Span(start=57, stop=75, type='PERS'), Span(start=98, stop=104, type='LOC'), Span(start=137, stop=141, type='ORG')])]
    ],
    [
        natasha,
        [NatashaMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', matches=[NatashaMatch(start=2, stop=5, type='Location', fact={'name': 'сша'}), NatashaMatch(start=38, stop=75, type='Location', fact={'name': 'соединённый штат томас джефферсон'}), NatashaMatch(start=57, stop=75, type='Name', fact={'last': 'джефферсон', 'first': 'томас'})])]
    ],
    [
        pullenti,
        [PullentiMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', matches=[PullentiMatch(referent=Referent(label='GEO', slots=[Slot(key='ALPHA2', value='US'), Slot(key='NAME', value='США'), Slot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), Slot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), Slot(key='TYPE', value='государство')]), span=PullentiSpan(start=2, stop=5), children=[]), PullentiMatch(referent=Referent(label='PERSON', slots=[Slot(key='SEX', value='MALE'), Slot(key='LASTNAME', value='ТОМАС'), Slot(key='FIRSTNAME', value='ДЖЕФФЕРСОН'), Slot(key='ATTRIBUTE', value=Referent(label='PERSONPROPERTY', slots=[Slot(key='REF', value=Referent(label='GEO', slots=[Slot(key='ALPHA2', value='US'), Slot(key='NAME', value='США'), Slot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), Slot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), Slot(key='TYPE', value='государство')])), Slot(key='NAME', value='третий президент')]))]), span=PullentiSpan(start=18, stop=75), children=[PullentiMatch(referent=Referent(label='PERSONPROPERTY', slots=[Slot(key='REF', value=Referent(label='GEO', slots=[Slot(key='ALPHA2', value='US'), Slot(key='NAME', value='США'), Slot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), Slot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), Slot(key='TYPE', value='государство')])), Slot(key='NAME', value='третий президент')]), span=PullentiSpan(start=18, stop=56), children=[PullentiMatch(referent=Referent(label='GEO', slots=[Slot(key='ALPHA2', value='US'), Slot(key='NAME', value='США'), Slot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), Slot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), Slot(key='TYPE', value='государство')]), span=PullentiSpan(start=38, stop=56), children=[])])]), PullentiMatch(referent=Referent(label='GEO', slots=[Slot(key='TYPE', value='штат'), Slot(key='NAME', value='ТЕХАС')]), span=PullentiSpan(start=98, stop=104), children=[]), PullentiMatch(referent=Referent(label='ORGANIZATION', slots=[Slot(key='PROFILE', value='Media'), Slot(key='NAME', value='LIFE')]), span=PullentiSpan(start=137, stop=141), children=[])])]
    ],
    [
        texterra,
        [TexterraMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', spans=[Span(start=2, stop=5, type='GPE_COUNTRY'), Span(start=38, stop=56, type='GPE_COUNTRY'), Span(start=57, stop=75, type='PERSON'), Span(start=98, stop=104, type='GPE_STATE_PROVINCE')])]
    ],
    [
        tomita,
        [TomitaMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', facts=[TomitaFact(start=57, stop=75, first='ТОМАС', last='ДЖЕФФЕРСОН', middle=None, known_surname=False)])]
    ]
]


@pytest.mark.int
@pytest.mark.parametrize('module, etalon', TESTS)
def test_zoo(module, etalon):
    try:
        module.start()
        guess = list(module.call(TEXTS))
        assert guess == etalon
    except:
        raise
    finally:
        module.stop()
