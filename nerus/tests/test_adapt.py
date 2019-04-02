
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
from nerus.sources.wikiner import WikinerMarkup
from nerus.sources.gareev import GareevMarkup


DEEPPALVOL_TESTS = [
    [
        DeeppavlovMarkup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PER'), Span(start=90, stop=101, type='PER'), Span(start=124, stop=140, type='ORG'), Span(start=141, stop=146, type='LOC'), Span(start=157, stop=168, type='ORG')]),
        Markup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PER'), Span(start=90, stop=101, type='PER'), Span(start=124, stop=140, type='ORG'), Span(start=141, stop=146, type='LOC'), Span(start=157, stop=168, type='ORG')])
    ],
    [
        DeeppavlovMarkup(text='Два кинопроекта продюсерского центра "Ленфильм" - лирическая комедия "Трек" Ильи Северова и сказка "Самый рыжий лис" Александры Стреляной - получили поддержку Министерства культуры РФ.', spans=[Span(start=38, stop=47, type='ORG'), Span(start=76, stop=89, type='PER'), Span(start=117, stop=137, type='PER'), Span(start=159, stop=180, type='ORG'), Span(start=181, stop=183, type='LOC')]),
        Markup(text='Два кинопроекта продюсерского центра "Ленфильм" - лирическая комедия "Трек" Ильи Северова и сказка "Самый рыжий лис" Александры Стреляной - получили поддержку Министерства культуры РФ.', spans=[Span(start=38, stop=46, type='ORG'), Span(start=76, stop=89, type='PER'), Span(start=117, stop=137, type='PER'), Span(start=159, stop=180, type='ORG'), Span(start=181, stop=183, type='LOC')])
    ]
]
MITIE_TESTS = [
    [
        MitieMarkup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PERS'), Span(start=90, stop=101, type='LOC'), Span(start=141, stop=146, type='LOC')]),
        Markup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PER'), Span(start=90, stop=101, type='LOC'), Span(start=141, stop=146, type='LOC')])
    ],
    [
        MitieMarkup(text='О великом британском учёном, которому в этом году исполнилось 200 лет, читайте в статье «2009-й — год Чарльза Дарвина».', spans=[Span(start=88, stop=95, type='ORG'), Span(start=102, stop=118, type='PERS')]),
        Markup(text='О великом британском учёном, которому в этом году исполнилось 200 лет, читайте в статье «2009-й — год Чарльза Дарвина».', spans=[Span(start=89, stop=95, type='ORG'), Span(start=102, stop=117, type='PER')])
    ]
]
NATASHA_TESTS = [
    [
        NatashaMarkup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', matches=[NatashaMatch(start=52, stop=59, type='Location', fact={'name': 'украина'}), NatashaMatch(start=60, stop=76, type='Name', fact={'first': 'пётр', 'last': 'порошенко'}), NatashaMatch(start=90, stop=101, type='Name', fact={'first': 'варфоломей'}), NatashaMatch(start=141, stop=146, type='Location', fact={'name': 'киев'}), NatashaMatch(start=157, stop=168, type='Organisation', fact={'name': 'РИА Новости'})]),
        Markup(text='«Объединительный собор», инициированный президентом Украины Петром Порошенко и патриархом Варфоломеем, пройдет 15 декабря в Софийском соборе Киева, передает РИА Новости.', spans=[Span(start=52, stop=59, type='LOC'), Span(start=60, stop=76, type='PER'), Span(start=90, stop=101, type='PER'), Span(start=141, stop=146, type='LOC'), Span(start=157, stop=168, type='ORG')])
    ],
    [
        NatashaMarkup(text='Исполнительный директор Молочного союза России Владимир Лабинов , считает , что факт демпинга доказать будет сложно .', matches=[NatashaMatch(start=40, stop=46, type='Location', fact={'name': 'россия'}), NatashaMatch(start=47, stop=55, type='Location', fact={'name': 'владимир'}), NatashaMatch(start=47, stop=63, type='Name', fact={'last': 'лабинов', 'first': 'владимир'})]),
        Markup(text='Исполнительный директор Молочного союза России Владимир Лабинов , считает , что факт демпинга доказать будет сложно .', spans=[Span(start=40, stop=46, type='LOC'), Span(start=47, stop=63, type='PER')])
    ]
]
TEXTERRA_TESTS = [
    [
        TexterraMarkup(text='Подтверждения этих сведений нет, но, как передает РИА Новости со ссылкой на ФСБ России, пограничники, применив оружие, задержали в Черном море в районе Керченского пролива три корабля Военно-морских сил Украины — катера «Бердянск» и «Никополь», а также буксир «Яны Капу».', spans=[Span(start=50, stop=61, type='ORGANIZATION_CORPORATION'), Span(start=76, stop=79, type='ORGANIZATION_POLITICAL'), Span(start=80, stop=86, type='GPE_COUNTRY'), Span(start=131, stop=142, type='LOCATION_LAKE_SEA_OCEAN'), Span(start=152, stop=171, type='FACILITY'), Span(start=221, stop=229, type='GPE_CITY'), Span(start=261, stop=269, type='PERSON')]),
        Markup(text='Подтверждения этих сведений нет, но, как передает РИА Новости со ссылкой на ФСБ России, пограничники, применив оружие, задержали в Черном море в районе Керченского пролива три корабля Военно-морских сил Украины — катера «Бердянск» и «Никополь», а также буксир «Яны Капу».', spans=[Span(start=50, stop=61, type='ORG'), Span(start=76, stop=79, type='ORG'), Span(start=80, stop=86, type='LOC'), Span(start=131, stop=142, type='LOC'), Span(start=221, stop=229, type='LOC'), Span(start=261, stop=269, type='PER')])
    ],
    [
        TexterraMarkup(text='Вместе с сайтами партнеров ее контент собирает 75 миллионов просмотров в месяц, сообщил собеседник «Коммерсант».', spans=[Span(start=100, stop=111, type='ORGANIZATION_POLITICAL')]),
        Markup(text='Вместе с сайтами партнеров ее контент собирает 75 миллионов просмотров в месяц, сообщил собеседник «Коммерсант».', spans=[Span(start=100, stop=110, type='ORG')])
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
    ],
    [
        Ne5Markup(id='11_01_13b', text='С 1992 года работал в Волгоградском коммерческом лицее, Молодежном центре культуры и кино "Россия", ЗАО ТК "Телемир".', spans=[Ne5Span(index='T8', type='ORG', start=22, stop=54, text='Волгоградском коммерческом лицее'), Ne5Span(index='T9', type='ORG', start=56, stop=98, text='Молодежном центре культуры и кино "Россия"'), Ne5Span(index='T10', type='ORG', start=100, stop=116, text='ЗАО ТК "Телемир"')]),
        Markup(text='С 1992 года работал в Волгоградском коммерческом лицее, Молодежном центре культуры и кино "Россия", ЗАО ТК "Телемир".', spans=[Span(start=22, stop=54, type='ORG'), Span(start=56, stop=98, type='ORG'), Span(start=100, stop=116, type='ORG')])
    ]
]
WIKINER_TESTS = [
    [
        WikinerMarkup(text='На севере граничит с Латвией , на востоке -- с Белоруссией , на юго-западе -- c Польшей и Калининградской областью России .', spans=[Span(start=21, stop=28, type='LOC'), Span(start=47, stop=58, type='ORG'), Span(start=80, stop=87, type='LOC'), Span(start=90, stop=114, type='PER'), Span(start=115, stop=121, type='MISC')]),
        Markup(text='На севере граничит с Латвией , на востоке -- с Белоруссией , на юго-западе -- c Польшей и Калининградской областью России .', spans=[Span(start=21, stop=28, type='LOC'), Span(start=47, stop=58, type='ORG'), Span(start=80, stop=87, type='LOC'), Span(start=90, stop=114, type='PER')]),
    ],
    [
        WikinerMarkup(text='В 1993 году журнал " Nature " опубликовал информацию о сделанном на острове Врангеля потрясающем открытии .', spans=[Span(start=21, stop=27, type='MISC'), Span(start=68, stop=84, type='LOC')]),
        Markup(text='В 1993 году журнал " Nature " опубликовал информацию о сделанном на острове Врангеля потрясающем открытии .', spans=[Span(start=68, stop=84, type='LOC')])
    ]
]
GAREEV_TESTS = [
    [
        GareevMarkup(text='После этого Росавиация ограничила полеты « ВИМ-Авиа » в Европу , но разрешила внутрироссийские полеты « из-за разницы в сертификационных требованиях России и Европы » .', spans=[Span(start=12, stop=22, type='ORG'), Span(start=41, stop=53, type='ORG')]),
        Markup(text='После этого Росавиация ограничила полеты « ВИМ-Авиа » в Европу , но разрешила внутрироссийские полеты « из-за разницы в сертификационных требованиях России и Европы » .', spans=[Span(start=12, stop=22, type='ORG'), Span(start=43, stop=51, type='ORG')])
    ],
    [
        GareevMarkup(text='Операционная прибыль News Corp . составила $ 4,2 млрд , из них за счет издательского бизнеса компания получила лишь $ 458 млн .', spans=[Span(start=21, stop=32, type='ORG')]),
        Markup(text='Операционная прибыль News Corp . составила $ 4,2 млрд , из них за счет издательского бизнеса компания получила лишь $ 458 млн .', spans=[Span(start=21, stop=30, type='ORG')])
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
    + WIKINER_TESTS
    + GAREEV_TESTS
)


@pytest.mark.parametrize('markup, etalon', TESTS)
def test_serialization(markup, etalon):
    guess = markup.adapted
    assert guess == etalon
