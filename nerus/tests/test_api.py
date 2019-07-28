
from nerus.path import (
    join_path,
    get_dir
)
from nerus.load import load_norm
from nerus.markup import Markup
from nerus.span import Span


DATA_DIR = join_path(get_dir(__file__), 'data')
NORM = join_path(DATA_DIR, 'test.jsonl.gz')

ETALON = Markup(text='Вице-премьер по социальным вопросам Татьяна Голикова рассказала, в каких регионах России зафиксирована наиболее высокая смертность от рака, сообщает РИА Новости. По словам Голиковой, чаще всего онкологические заболевания становились причиной смерти в Псковской, Тверской, Тульской и Орловской областях, а также в Севастополе. Вице-премьер напомнила, что главные факторы смертности в России — рак и болезни системы кровообращения. В начале года стало известно, что смертность от онкологических заболеваний среди россиян снизилась впервые за три года. По данным Росстата, в 2017 году от рака умерли 289 тысяч человек. Это на 3,5 процента меньше, чем годом ранее.', spans=[Span(start=36, stop=52, type='PER'), Span(start=82, stop=88, type='LOC'), Span(start=149, stop=160, type='ORG'), Span(start=172, stop=181, type='PER'), Span(start=251, stop=260, type='LOC'), Span(start=262, stop=270, type='LOC'), Span(start=272, stop=280, type='LOC'), Span(start=283, stop=301, type='LOC'), Span(start=313, stop=324, type='LOC'), Span(start=383, stop=389, type='LOC'), Span(start=560, stop=568, type='ORG')])


# Should work in isolation (just requirements/main.txt)
def test_load_norm():
    record = next(load_norm(NORM))
    assert record == ETALON
