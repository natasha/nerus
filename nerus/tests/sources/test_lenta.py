
from nerus.path import (
    join_path,
    get_dir
)
from nerus.const import LENTA_FILENAME
from nerus.sources.lenta import (
    LentaRecord,
    LentaSource
)


# gzcat lenta-ru-news.csv.gz | head -2 | gzip > ../nerus/tests/corpora/data/lenta-ru-news.csv.gz
DATA_DIR = join_path(get_dir(__file__), 'data')
ETALON = [
    LentaRecord(url='https://lenta.ru/news/2018/12/14/cancer/', title='Названы регионы России с\xa0самой высокой смертностью от\xa0рака', text='Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в каких регионах России зафиксирована наиболее высокая смертность от рака, сообщает РИА Новости. По словам Голиковой, чаще всего онкологические заболевания становились причиной смерти в Псковской, Тверской, Тульской и Орловской областях, а также в Севастополе. Вице-премьер напомнила, что главные факторы смертности в России — рак и болезни системы кровообращения. В начале года стало известно, что смертность от онкологических заболеваний среди россиян снизилась впервые за три года. По данным Росстата, в 2017 году от рака умерли 289 тысяч человек. Это на 3,5 процента меньше, чем годом ранее.', topic='Россия', tags='Общество')
]


def test_load():
    path = join_path(DATA_DIR, LENTA_FILENAME)
    guess = list(LentaSource.load(path))
    assert guess == ETALON
