
from nerus.const import (
    LOC,
    ORG,
    PER
)
from nerus.span import strip_spans
from nerus.markup import Markup

from .common import (
    QUOTES, SPACES,
    adapt_spans
)


TYPES = {
    'PERSON': PER,  # 9119

    'GPE_COUNTRY': LOC,  # 3797
    'GPE_STATE_PROVINCE': LOC,  # 1341
    'GPE_CITY': LOC,  # 1329
    'GPE_OTHER': LOC,  # 59
    'LOCATION_LAKE_SEA_OCEAN': LOC,  # 12
    'LOCATION_OTHER': LOC,  # 10
    'LOCATION_REGION': LOC,  # 113
    'LOCATION_CONTINENT': LOC,  # 48
    'LOCATION_RIVER': LOC,  # 18

    'ORGANIZATION_POLITICAL': ORG,  # 2311
    'ORGANIZATION_CORPORATION': ORG,  # 1484
    'ORGANIZATION_OTHER': ORG,  # 689
    'ORGANIZATION_EDUCATIONAL': ORG,  # 213

    # For better precision do not treat
    # WORK_OF_ART, FACILITY as orgs, since
    # it not alway true (Черная кошка for example)

    # РБК daily, The Wall Street Journal
    # News of The World
    # 'WORK_OF_ART': ORG,  # 236
    # Русале, Лужников, Кремля, Домодедово
    # Пражском Граде  <- sometimes GEO
    # 'FACILITY': ORG,  # 200

    # 'NORP_RELIGION',  # 24 мусульманским, Бог, еврейских
    # 'NORP_NATIONALITY',  # 21 египтян, мордва
    # 'NORP_POLITICAL',  # 3 Лейбористы, социалистов
    # 'NORP_OTHER',  # 2 масон, афроамериканца

    # 'EVENT', # 134 Олимпиады в Сочи, День России, ВОВ
    # 'PRODUCT',  # 103 Google Maps, iOS, iPhone, истребителей F-16
    # 'SUBSTANCE',  # 41 никеля, алюминия, нефть
    # 'DISEASE',  # 22 ВИЭ, наркомании, СПИД, шизофренией
    # 'GAME',  # 15 футбольного, теннисист
    # 'LANGUAGE',  # 10 русскому языку, нидерландской, абхазского
    # 'ANIMAL',  # 5 Черепаха, Человек, заяц
    # 'PLANT',  # 1 табак
}


def adapt(markup):
    spans = list(strip_spans(markup.spans, markup.text, QUOTES + SPACES))
    spans = list(adapt_spans(spans, markup.text, TYPES))
    return Markup(markup.text, spans)
