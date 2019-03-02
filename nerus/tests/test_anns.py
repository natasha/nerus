

import pytest

from nerus.anns import (
    deeppavlov,
    mitie,
    natasha,
    pullenti,
    texterra,
    tomita
)
from nerus.span import Span
from nerus.anns.deeppavlov import DeeppavlovMarkup
from nerus.anns.mitie import MitieMarkup
from nerus.anns.natasha import (
    NatashaMarkup,
    NatashaMatch
)
from nerus.anns.pullenti import (
    PullentiMarkup,
    PullentiMatch,
    PullentiReferent,
    PullentiSlot,
    PullentiSpan
)
from nerus.anns.texterra import TexterraMarkup
from nerus.anns.tomita import (
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
        [PullentiMarkup(text='В США прядь волос третьего президента Соединенных Штатов Томаса Джефферсона продали на аукционе в Техасе за 6,9 тысячи долларов передает Life.', matches=[PullentiMatch(referent=PullentiReferent(label='GEO', slots=[PullentiSlot(key='ALPHA2', value='US'), PullentiSlot(key='NAME', value='США'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), PullentiSlot(key='TYPE', value='государство')]), span=PullentiSpan(start=2, stop=5), children=[]), PullentiMatch(referent=PullentiReferent(label='PERSON', slots=[PullentiSlot(key='SEX', value='MALE'), PullentiSlot(key='LASTNAME', value='ТОМАС'), PullentiSlot(key='FIRSTNAME', value='ДЖЕФФЕРСОН'), PullentiSlot(key='ATTRIBUTE', value=PullentiReferent(label='PERSONPROPERTY', slots=[PullentiSlot(key='REF', value=PullentiReferent(label='GEO', slots=[PullentiSlot(key='ALPHA2', value='US'), PullentiSlot(key='NAME', value='США'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), PullentiSlot(key='TYPE', value='государство')])), PullentiSlot(key='NAME', value='третий президент')]))]), span=PullentiSpan(start=18, stop=75), children=[PullentiMatch(referent=PullentiReferent(label='PERSONPROPERTY', slots=[PullentiSlot(key='REF', value=PullentiReferent(label='GEO', slots=[PullentiSlot(key='ALPHA2', value='US'), PullentiSlot(key='NAME', value='США'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), PullentiSlot(key='TYPE', value='государство')])), PullentiSlot(key='NAME', value='третий президент')]), span=PullentiSpan(start=18, stop=56), children=[PullentiMatch(referent=PullentiReferent(label='GEO', slots=[PullentiSlot(key='ALPHA2', value='US'), PullentiSlot(key='NAME', value='США'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ'), PullentiSlot(key='NAME', value='СОЕДИНЕННЫЕ ШТАТЫ АМЕРИКИ'), PullentiSlot(key='TYPE', value='государство')]), span=PullentiSpan(start=38, stop=56), children=[])])]), PullentiMatch(referent=PullentiReferent(label='GEO', slots=[PullentiSlot(key='TYPE', value='штат'), PullentiSlot(key='NAME', value='ТЕХАС')]), span=PullentiSpan(start=98, stop=104), children=[]), PullentiMatch(referent=PullentiReferent(label='ORGANIZATION', slots=[PullentiSlot(key='PROFILE', value='Media'), PullentiSlot(key='NAME', value='LIFE')]), span=PullentiSpan(start=137, stop=141), children=[])])]
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
@pytest.mark.parametrize('service, etalon', TESTS)
def test_anns(service, etalon):
    try:
        service.start()
        guess = list(service.call(TEXTS))
        assert guess == etalon
    except:
        raise
    finally:
        service.stop()
