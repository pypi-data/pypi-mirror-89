from dataclasses import asdict

import datetime
from functools import wraps



Datetime = datetime.datetime


class _Empty: ...

def operation(func):
    @wraps(func)
    def wrapper(instance, item, session=None):
        instance.ensure_table_exists(item)

        commit = session is None
        session = session
        ret = func(instance, item, session)
