
from nerus.path import (
    join_path,
    get_dir
)
from nerus.const import (
    FACTRU_DIR,
    FACTRU_DEVSET
)
from nerus.sources.factru import (
    FactruMarkup,
    FactruObject,
    FactruSpan,
    FactruSource
)


DATA_DIR = join_path(get_dir(__file__), 'data')
ETALON = [
    FactruMarkup(id='58', text='Встреча с послом Италии в миде Грузии\n\nПо инициативе итальянской стороны чрезвычайный и полномочный посол Италии в Грузии Виторио Сандали встретился с заместителем министра иностранных дел Грузии Александром Налбандовым. Предметом обсуждения стали вопросы сотрудничества в международных организациях.\n', objects=[FactruObject(id='16972', type='LocOrg', spans=[FactruSpan(id='32962', type='loc_name', start=17, stop=23)]), FactruObject(id='16975', type='Org', spans=[FactruSpan(id='32963', type='org_name', start=26, stop=30), FactruSpan(id='32965', type='loc_name', start=31, stop=37)]), FactruObject(id='16974', type='LocOrg', spans=[FactruSpan(id='32965', type='loc_name', start=31, stop=37)]), FactruObject(id='16967', type='LocOrg', spans=[FactruSpan(id='32951', type='loc_name', start=106, stop=112)]), FactruObject(id='16968', type='LocOrg', spans=[FactruSpan(id='32952', type='loc_name', start=115, stop=121)]), FactruObject(id='16969', type='Person', spans=[FactruSpan(id='32953', type='name', start=122, stop=129), FactruSpan(id='32954', type='surname', start=130, stop=137)]), FactruObject(id='16970', type='LocOrg', spans=[FactruSpan(id='32955', type='loc_name', start=189, stop=195)]), FactruObject(id='16971', type='Person', spans=[FactruSpan(id='32956', type='name', start=196, stop=207), FactruSpan(id='32957', type='surname', start=208, stop=219)])])
]


def test_load():
    dir = join_path(DATA_DIR, FACTRU_DIR)
    guess = list(FactruSource.load(dir, sets=[FACTRU_DEVSET]))
    assert guess == ETALON
