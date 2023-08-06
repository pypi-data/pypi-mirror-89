import datetime
from dataclasses import dataclass, field
from typing import Union, Text
from unittest import mock


try:
    import aws_cdk.core as cdk
    import aws_cdk.aws_s3 as s3
    import aws_cdk.aws_glue as glue
    import aws_cdk.aws_athena as athena
    import jsii
    Type = Union[type, glue.Type]

except ImportError:
    cdk = mock.Mock()
    s3 = mock.Mock()
    glue = mock.Mock()
    athena = mock.Mock()
    Type = type

Datetime = datetime.datetime
Date = datetime.date


def array(item_type: glue.Type) -> glue.Type:
    return jsii.sinvoke(glue.Schema, "array", [item_type])


def glue_map(key_type, value_type):
    return jsii.sinvoke(glue.Schema, "map", [key_type, value_type])
