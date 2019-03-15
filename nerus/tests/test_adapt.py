
import pytest

from nerus.markup import Markup
from nerus.span import Span
from nerus.annotators.deeppavlov import DeeppavlovMarkup
from nerus.annotators.natasha import (
    NatashaMarkup,
    NatashaMatch
)
from nerus.annotators.mitie import MitieMarkup
from nerus.annotators.texterra import TexterraMarkup
from nerus.annotators.tomita import (
    TomitaMarkup,
    TomitaFact
)
from nerus.annotators.pullenti import (
    PullentiMarkup,
    PullentiMatch,
    PullentiSpan
)
from pullenti_client.referent import Referent
from nerus.sources.ne5 import (
    Ne5Markup,
    Ne5Span
)
from nerus.sources.factru import (
    FactruMarkup,
    FactruObject,
    FactruSpan
)


DEEPPALVOL_TESTS = [
    [
        DeeppavlovMarkup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PER'), Span(start=90, stop=101, type='PER'), Span(start=124, stop=140, type='ORG'), Span(start=141, stop=146, type='LOC'), Span(start=157, stop=168, type='ORG')]),
        Markup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PER'), Span(start=90, stop=101, type='PER'), Span(start=124, stop=140, type='ORG'), Span(start=141, stop=146, type='LOC'), Span(start=157, stop=168, type='ORG')])
    ],
]
MITIE_TESTS = [
    [
        MitieMarkup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PERS'), Span(start=90, stop=101, type='LOC'), Span(start=141, stop=146, type='LOC')]),
        Markup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PER'), Span(start=90, stop=101, type='LOC'), Span(start=141, stop=146, type='LOC')])
    ],
]
NATASHA_TESTS = [
    [
        NatashaMarkup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', matches=[NatashaMatch(start=52, stop=59, type='Location', fact={'name': 'украина'}), NatashaMatch(start=60, stop=76, type='Name', fact={'first': 'пётр', 'last': 'порошенко'}), NatashaMatch(start=90, stop=101, type='Name', fact={'first': 'варфоломей'}), NatashaMatch(start=141, stop=146, type='Location', fact={'name': 'киев'}), NatashaMatch(start=157, stop=168, type='Organisation', fact={'name': 'РИА Новости'})]),
        Markup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PER'), Span(start=90, stop=101, type='PER'), Span(start=141, stop=146, type='LOC'), Span(start=157, stop=168, type='ORG')])
    ],
    [
        NatashaMarkup(text='Ранее глава Минэнерго России Александр Новак сообщал, что переговоры, возможно, пройдут во второй половине января, добавляет РИА Новости.', matches=[NatashaMatch(start=12, stop=38, type='Organisation', fact={'name': 'Минэнерго России Александр'}), NatashaMatch(start=22, stop=28, type='Location', fact={'name': 'россия'}), NatashaMatch(start=29, stop=44, type='Name', fact={'first': 'александр', 'last': 'новак'}), NatashaMatch(start=39, stop=44, type='Organisation', fact={'name': 'Новак'}), NatashaMatch(start=125, stop=136, type='Organisation', fact={'name': 'РИА Новости'})]),
        Markup(text='Ранее глава Минэнерго России Александр Новак сообщал, что переговоры, возможно, пройдут во второй половине января, добавляет РИА Новости.', spans=[Span(start=12, stop=21, type='ORG'), Span(start=22, stop=28, type='LOC'), Span(start=29, stop=38, type='PER'), Span(start=39, stop=44, type='ORG'), Span(start=125, stop=136, type='ORG')])
    ]
]
TEXTERRA_TESTS = [
    [
        TexterraMarkup(text='Подтверждения этих сведений нет, но, как передает РИА Новости со ссылкой на ФСБ России, пограничники, применив оружие, задержали в Черном море в районе Керченского пролива три корабля Военно-морских сил Украины — катера «Бердянск» и «Никополь», а также буксир «Яны Капу».', spans=[Span(start=50, stop=61, type='ORGANIZATION_CORPORATION'), Span(start=76, stop=79, type='ORGANIZATION_POLITICAL'), Span(start=80, stop=86, type='GPE_COUNTRY'), Span(start=131, stop=142, type='LOCATION_LAKE_SEA_OCEAN'), Span(start=152, stop=171, type='FACILITY'), Span(start=221, stop=229, type='GPE_CITY'), Span(start=261, stop=269, type='PERSON')]),
        Markup(text='Подтверждения этих сведений нет, но, как передает РИА Новости со ссылкой на ФСБ России, пограничники, применив оружие, задержали в Черном море в районе Керченского пролива три корабля Военно-морских сил Украины — катера «Бердянск» и «Никополь», а также буксир «Яны Капу».', spans=[Span(start=50, stop=61, type='ORG'), Span(start=76, stop=79, type='ORG'), Span(start=80, stop=86, type='LOC'), Span(start=131, stop=142, type='LOC'), Span(start=152, stop=171, type='ORG'), Span(start=221, stop=229, type='LOC'), Span(start=261, stop=269, type='PER')])
    ]
]
TOMITA_TESTS = [
    [
        TomitaMarkup(text='В своем послании он также осудил снятие анафемы с предстоятеля неканонической УПЦ Киевского патриархата Филарета.', facts=[TomitaFact(start=104, stop=112, first='ФИЛАРЕТ', last=None, middle=None, known_surname=False)]),
        Markup(text='В своем послании он также осудил снятие анафемы с предстоятеля неканонической УПЦ Киевского патриархата Филарета.', spans=[Span(start=104, stop=112, type='PER')])
    ]
]
PULLENTI_TESTS = [
    [
        PullentiMarkup(text='Об этом в Facebook сообщил начальник Генштаба Вооруженных сил Украины (ВСУ) Виктор Муженко.', matches=[PullentiMatch(referent=Referent(label='ORGANIZATION', slots=[]), span=PullentiSpan(start=10, stop=18), children=[]), PullentiMatch(referent=Referent(label='PERSON', slots=[]), span=PullentiSpan(start=27, stop=90), children=[PullentiMatch(referent=Referent(label='PERSONPROPERTY', slots=[]), span=PullentiSpan(start=27, stop=75), children=[PullentiMatch(referent=Referent(label='ORGANIZATION', slots=[]), span=PullentiSpan(start=37, stop=75), children=[PullentiMatch(referent=Referent(label='ORGANIZATION', slots=[]), span=PullentiSpan(start=37, stop=69), children=[PullentiMatch(referent=Referent(label='ORGANIZATION', slots=[]), span=PullentiSpan(start=46, stop=69), children=[PullentiMatch(referent=Referent(label='GEO', slots=[]), span=PullentiSpan(start=62, stop=69), children=[])])]), PullentiMatch(referent=Referent(label='ORGANIZATION', slots=[]), span=PullentiSpan(start=70, stop=75), children=[])])])])]),
        Markup(text='Об этом в Facebook сообщил начальник Генштаба Вооруженных сил Украины (ВСУ) Виктор Муженко.', spans=[Span(start=10, stop=18, type='ORG'), Span(start=37, stop=45, type='ORG'), Span(start=46, stop=61, type='ORG'), Span(start=62, stop=69, type='LOC'), Span(start=71, stop=74, type='ORG'), Span(start=76, stop=90, type='PER')])
    ]
]
FACTRU_TESTS = [
    [
        FactruMarkup(id='349', text='Глава палестинской делегации на переговорах Саеб Эрекат призвал ООН «ответить на односторонние действия Израиля признанием Палестинского государства в границах 67-го года со столицей в Восточном Иерусалиме».', objects=[FactruObject(id='43890', type='Org', spans=[FactruSpan(id='28592', type='org_descr', start=6, stop=28), FactruSpan(id='73775', type='geo_adj', start=6, stop=18), FactruSpan(id='73776', type='org_descr', start=19, stop=28)]), FactruObject(id='14157', type='Person', spans=[FactruSpan(id='28593', type='name', start=44, stop=48), FactruSpan(id='28594', type='surname', start=49, stop=55)]), FactruObject(id='14158', type='Org', spans=[FactruSpan(id='28595', type='org_name', start=64, stop=67)]), FactruObject(id='14159', type='LocOrg', spans=[FactruSpan(id='28596', type='loc_name', start=104, stop=111)]), FactruObject(id='43889', type='LocOrg', spans=[FactruSpan(id='28597', type='loc_name', start=123, stop=148), FactruSpan(id='28598', type='loc_descr', start=137, stop=148), FactruSpan(id='73774', type='geo_adj', start=123, stop=136)]), FactruObject(id='14161', type='Location', spans=[FactruSpan(id='28599', type='loc_name', start=185, stop=205), FactruSpan(id='28600', type='loc_name', start=195, stop=205)])]),
        Markup(text='Глава палестинской делегации на переговорах Саеб Эрекат призвал ООН «ответить на односторонние действия Израиля признанием Палестинского государства в границах 67-го года со столицей в Восточном Иерусалиме».', spans=[Span(start=44, stop=55, type='PER'), Span(start=64, stop=67, type='ORG'), Span(start=104, stop=111, type='LOC'), Span(start=123, stop=148, type='LOC'), Span(start=185, stop=205, type='LOC')])
    ]
]
NE5_TESTS = [
    [
        Ne5Markup(id='shojgu1', text='Назначение Сергея Шойгу министром обороны России поможет решению проблемы военных городков в Подмосковье, заявил РИА Новости председатель Мособлдумы Игорь Брынцалов.', spans=[Ne5Span(index='T3', type='PER', start=11, stop=23, text='Сергея Шойгу'), Ne5Span(index='T4', type='GEOPOLIT', start=42, stop=48, text='России'), Ne5Span(index='T5', type='LOC', start=93, stop=104, text='Подмосковье'), Ne5Span(index='T6', type='MEDIA', start=113, stop=124, text='РИА Новости'), Ne5Span(index='T7', type='ORG', start=138, stop=148, text='Мособлдумы'), Ne5Span(index='T8', type='PER', start=149, stop=164, text='Игорь Брынцалов')]),
        Markup(text='Назначение Сергея Шойгу министром обороны России поможет решению проблемы военных городков в Подмосковье, заявил РИА Новости председатель Мособлдумы Игорь Брынцалов.', spans=[Span(start=11, stop=23, type='PER'), Span(start=42, stop=48, type='LOC'), Span(start=93, stop=104, type='LOC'), Span(start=113, stop=124, type='ORG'), Span(start=138, stop=148, type='ORG'), Span(start=149, stop=164, type='PER')])
    ]
]
TESTS = (
    DEEPPALVOL_TESTS
    + MITIE_TESTS
    + NATASHA_TESTS
    + TEXTERRA_TESTS
    + TOMITA_TESTS
    + PULLENTI_TESTS
    + FACTRU_TESTS
    + NE5_TESTS
)


@pytest.mark.parametrize('markup, etalon', TESTS)
def test_serialization(markup, etalon):
    guess = markup.adapted
    assert guess == etalon
