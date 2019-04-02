
from nerus.const import (
    ORG,
    PER,
    LOC
)
from nerus.markup import Markup
from nerus.span import (
    Span,
    filter_overlapping
)

from .common import adapt_spans


# Org 2821
#     org_name 2333
#     org_descr 1700
#     loc_name 211
#     geo_adj 83
#     loc_descr 25
#     surname 17
#     job 7
#     name 5
#     nickname 2
# Person 2129
#     surname 1945
#     name 1336
#     nickname 65
#     patronymic 42
# LocOrg 1399
#     loc_name 1259
#     geo_adj 108
#     loc_descr 88
#     org_name 20
#     org_descr 9
# Location 1257
#     loc_name 1175
#     loc_descr 249
#     geo_adj 49
#     org_name 18
#     org_descr 15
#     surname 4
#     nickname 2
#     name 2
# Project 22 Вечерний Ургант, Пусть говорят, КВН, Пока все дома
# Facility 2 сайта Caramba TV


TYPES = {
    'Org': ORG,
    'Person': PER,
    'LocOrg': LOC,
    'Location': LOC
}


def select_spans(markup):
    for object in markup.objects:
        type = object.type
        if type == 'Person':
            yield Span(object.start, object.stop, object.type)
        elif type == 'Org':
            spans = [_ for _ in object.spans if _.type == 'org_name']
            for span in filter_overlapping(spans):
                yield Span(span.start, span.stop, type)
        elif type in ('LocOrg', 'Location'):
            spans = [_ for _ in object.spans if _.type == 'loc_name']
            for span in filter_overlapping(spans):
                yield Span(span.start, span.stop, type)


def adapt(markup):
    spans = list(select_spans(markup))

    # мид Грузии
    # ORG-------
    #     LOC---
    spans = list(filter_overlapping(spans))

    spans = list(adapt_spans(spans, markup.text, TYPES))
    return Markup(markup.text, spans)
