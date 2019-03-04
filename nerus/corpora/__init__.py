
from .factru import FactruSchema
from .lenta import LentaSchema
from .ne5 import Ne5Schema


SCHEMAS = [
    FactruSchema,
    LentaSchema,
    Ne5Schema
]


def find(name):
    for schema in SCHEMAS:
        if schema.name == name:
            return schema
