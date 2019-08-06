
import pandas as pd

from nerus.const import (
    PER, LOC, ORG,
    WIKINER, GAREEV
)


def report_table(scores, sources, annotators, types=[PER, LOC, ORG]):
    data = []
    for source in sources:
        for annotator in annotators:
            for type in types:
                score = scores[source, annotator][type]
                data.append([source, annotator, type, score])
    table = pd.DataFrame(data, columns=['source', 'annotator', 'type', 'score'])
    table = table.set_index(['source', 'annotator', 'type']).unstack(['source', 'type'])

    table.columns = table.columns.droplevel()
    table.index.name = None

    columns = [
        (source, type)
        for source in sources
        for type in types
    ]
    table = table.reindex(index=annotators, columns=columns)

    return table


def format_score(value):
    if not value:
        return '-'
    return '{0:02d}'.format(int(value * 100))


def format_scores(scores):
    return '{prec}/{recall}/{f1}'.format(
        prec=format_score(scores.prec),
        recall=format_score(scores.recall),
        f1=format_score(scores.f1)
    )


def format_report(table):
    output = pd.DataFrame()
    for column in table.columns:
        output[column] = table[column].map(format_scores)

    output.columns = pd.MultiIndex.from_tuples(output.columns)
    output.columns.names = [None, 'prec/recall/f1,%']

    return output


def format_github_column(column):
    column = [
        (_.f1 if _ else None)
        for _ in column
    ]

    selection = None
    values = list(filter(None, column))
    if values:
        selection = max(values)

    for value in column:
        cell = ''
        if value:
            cell = '%.3f' % value
        if selection and value == selection:
            cell = '<b>%s</b>' % cell
        yield cell


def format_github_report(table):
    output = pd.DataFrame()
    for column in table.columns:
        source, type = column
        if source == WIKINER or (source == GAREEV and type == LOC):
            continue
        output[column] = list(format_github_column(table[column]))

    output.index = table.index
    output.columns = pd.MultiIndex.from_tuples(output.columns)
    output.columns.names = [None, 'f1']

    return output
