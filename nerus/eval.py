
from collections import defaultdict

from .const import (
    PER, ORG, LOC,
    I, O
)
from .utils import (
    Record,
    strict_zip
)
from .token import tokenize
from .span import select_type_spans
from .bio import (
    spans_io,
    parse_bio
)


TYPES = [PER, ORG, LOC]


class Score(Record):
    __attributes__ = [
        'prec_errors', 'prec_total',
        'recall_errors', 'recall_total',
    ]

    def __init__(self, prec_errors=0, prec_total=0, recall_errors=0, recall_total=0):
        self.prec_errors = prec_errors
        self.prec_total = prec_total
        self.recall_errors = recall_errors
        self.recall_total = recall_total

    @property
    def prec(self):
        if self.prec_total:
            return 1 - self.prec_errors / self.prec_total

    @property
    def recall(self):
        if self.recall_total:
            return 1 - self.recall_errors / self.recall_total

    @property
    def f1(self):
        p = self.prec
        r = self.recall
        if p is None or r is None:
            return
        return 2 * p * r / (p + r)

    def update(self, other):
        self.prec_errors += other.prec_errors
        self.prec_total += other.prec_total
        self.recall_errors += other.recall_errors
        self.recall_total += other.recall_total


def eval_score(tokens, guess, etalon, type):
    spans = list(select_type_spans(guess, type))
    guess_tags = list(spans_io(tokens, spans))
    spans = list(select_type_spans(etalon, type))
    etalon_tags = list(spans_io(tokens, spans))
    score = Score()
    for guess, etalon in strict_zip(guess_tags, etalon_tags):
        guess, _ = parse_bio(guess)
        etalon, _ = parse_bio(etalon)
        if guess == I:
            score.prec_total += 1
            if etalon == O:
                score.prec_errors += 1
        if etalon == I:
            score.recall_total += 1
            if guess == O:
                score.recall_errors += 1
    return score


def eval_markup(guess, etalon, types=TYPES):
    if guess.text != etalon.text:
        # super rare for deeppavlov guess is prefix of etalon
        return
    tokens = list(tokenize(guess.text))
    for type in types:
        score = eval_score(tokens, guess.spans, etalon.spans, type)
        yield type, score


def eval_markups(guesses, etalons, types=TYPES):
    scores = defaultdict(Score)
    for guess, etalon in strict_zip(guesses, etalons):
        for type, score in eval_markup(guess, etalon, types):
            scores[type].update(score)
    return dict(scores)
