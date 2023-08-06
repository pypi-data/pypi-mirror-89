from dataclasses import dataclass, field, Field
from typing import Text

from .compat import glue, Type
from .typemap import python_to_glue


def extract_meta(dt_field: Field):
    dt_meta = dt_field.metadata.copy()
    _meta = {}
    if isinstance(dt_meta, Column):
        _meta["column"] = dt_meta
    else:
        _meta = dt_meta.pop("monomer", _meta)
        for k in dt_meta:
            if k[:7] == "_monomer":
                _meta[k[7:]] = dt_meta[k]
    return _meta


@dataclass
class Column(object):
    name: Text
    type: Type = field(default=None)
    comment: Text = field(default="Monomer generated column")

    def to_glue(self):
        return glue.Column(name=self.name, type=self.type, comment=self.comment)

    @classmethod
    def from_field(cls, dt_field):
        meta = extract_meta(dt_field)
        column = meta.get("column", Column(dt_field.name))
        if column.name is None:
            column.name = dt_field.name
        if column.type is None:
            column.type = python_to_glue(dt_field.type)
        return column
