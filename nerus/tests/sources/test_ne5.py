
from nerus.path import (
    join_path,
    get_dir
)
from nerus.const import NE5_DIR
from nerus.sources.ne5 import (
    Ne5Markup,
    Ne5Span,
    Ne5Source
)


DATA_DIR = join_path(get_dir(__file__), 'data')
ETALON = [
    Ne5Markup(id='001', text='Россия рассчитывает на конструктивное воздействие США на Грузию\r\n\r\n04/08/2008 12:08\r\n\r\nМОСКВА, 4 авг - РИА Новости. Россия рассчитывает, что США воздействуют на Тбилиси в связи с обострением ситуации в зоне грузино-осетинского конфликта. Об этом статс-секретарь - заместитель министра иностранных дел России Григорий Карасин заявил в телефонном разговоре с заместителем госсекретаря США Дэниэлом Фридом.\r\n\r\n"С российской стороны выражена глубокая озабоченность в связи с новым витком напряженности вокруг Южной Осетии, противозаконными действиями грузинской стороны по наращиванию своих вооруженных сил в регионе, бесконтрольным строительством фортификационных сооружений", - говорится в сообщении.\r\n\r\n"Россия уже призвала Тбилиси к ответственной линии и рассчитывает также на конструктивное воздействие со стороны Вашингтона", - сообщил МИД России. ', spans=[Ne5Span(index='T1', type='GEOPOLIT', start=0, stop=6, text='Россия'), Ne5Span(index='T2', type='GEOPOLIT', start=50, stop=53, text='США'), Ne5Span(index='T3', type='GEOPOLIT', start=57, stop=63, text='Грузию'), Ne5Span(index='T4', type='LOC', start=87, stop=93, text='МОСКВА'), Ne5Span(index='T5', type='MEDIA', start=103, stop=114, text='РИА Новости'), Ne5Span(index='T6', type='GEOPOLIT', start=116, stop=122, text='Россия'), Ne5Span(index='T7', type='GEOPOLIT', start=141, stop=144, text='США'), Ne5Span(index='T8', type='GEOPOLIT', start=161, stop=168, text='Тбилиси'), Ne5Span(index='T9', type='GEOPOLIT', start=301, stop=307, text='России'), Ne5Span(index='T10', type='PER', start=308, stop=324, text='Григорий Карасин'), Ne5Span(index='T11', type='GEOPOLIT', start=383, stop=386, text='США'), Ne5Span(index='T12', type='PER', start=387, stop=402, text='Дэниэлом Фридом'), Ne5Span(index='T13', type='GEOPOLIT', start=505, stop=517, text='Южной Осетии'), Ne5Span(index='T14', type='GEOPOLIT', start=703, stop=709, text='Россия'), Ne5Span(index='T15', type='GEOPOLIT', start=723, stop=730, text='Тбилиси'), Ne5Span(index='T16', type='GEOPOLIT', start=815, stop=825, text='Вашингтона'), Ne5Span(index='T17', type='ORG', start=838, stop=841, text='МИД'), Ne5Span(index='T18', type='GEOPOLIT', start=842, stop=848, text='России')])
]


def test_load():
    dir = join_path(DATA_DIR, NE5_DIR)
    guess = list(Ne5Source.load(dir))
    assert guess == ETALON
