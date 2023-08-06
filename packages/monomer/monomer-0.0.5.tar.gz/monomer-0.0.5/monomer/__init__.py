import inspect
import logging
from dataclasses import fields, field
from itertools import chain
from typing import Text, List

from .column import Column
from .compat import cdk, glue, s3

logger = logging.getLogger("monomer")


class monomer_property(property):

    def __init__(self, prp_or_column):
        self._column = None
        if isinstance(prp_or_column, Column):
            self._column = prp_or_column
        else:
            super().__init__(prp_or_column)

    def __call__(self, prp, *args, **kwargs):
        return super().__init__(prp)

    @staticmethod
    def persisted_properties(datacls):
        for k, v in inspect.getmembers(datacls, lambda a: isinstance(a, monomer_property)):
            yield v.make_field(k)

    def make_field(self, k):
        f = field()
        f.name = k
        _type = inspect.signature(self.fget).return_annotation
        if _type is inspect.Signature.empty:
            _type = Text
        f.type = _type
        if self._column is not None:
            f.metadata["monomer"] = {"column": self._column}
        return f


class MonomerDatabase(cdk.Construct):

    def __init__(self, scope: cdk.Construct, id: Text, database_name: Text):
        super().__init__(scope, id)
        self.db = glue.Database(self, 'lads', database_name='lads')
        self.s3bucket = s3.Bucket(self, f"{database_name}-store",
                                  bucket_name=f"{database_name}-data-storage",
                                  block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                  encryption=s3.BucketEncryption.S3_MANAGED)
        self.tables: List[glue.Table] = []

    def add_table(self, datacls, bucket=None):
        dt_name = datacls.__name__
        columns = list(Column.from_field(dt_field)
                       for dt_field in chain(fields(datacls), monomer_property.persisted_properties(datacls)))
        table = glue.Table(self, f'{dt_name}Table',
                           database=self.db,
                           table_name=dt_name,
                           bucket=bucket or self.s3bucket,
                           s3_prefix=dt_name.lower() if bucket is None else '',
                           columns=list(col.to_glue() for col in columns),
                           data_format=glue.DataFormat.JSON)
        self.tables.append(table)
        return table
