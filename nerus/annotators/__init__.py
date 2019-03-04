
from .deeppavlov import DeeppavlovAnnotator
from .mitie import MitieAnnotator
from .natasha import NatashaAnnotator
from .pullenti import PullentiAnnotator
from .texterra import TexterraAnnotator
from .tomita import TomitaAnnotator


CONSTRUCTORS = [
    DeeppavlovAnnotator,
    MitieAnnotator,
    NatashaAnnotator,
    PullentiAnnotator,
    TexterraAnnotator,
    TomitaAnnotator
]


def find(name):
    for constructor in CONSTRUCTORS:
        if constructor.name == name:
            return constructor
