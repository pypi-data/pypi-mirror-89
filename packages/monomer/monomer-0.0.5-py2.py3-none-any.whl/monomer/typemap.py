from typing import Union, Text, get_args, get_origin

from .compat import glue, Datetime, Date, array, glue_map

VARCHAR_LEN = 256

glue_type_map = {
    Text: glue.Schema.STRING,
    Datetime: glue.Schema.TIMESTAMP,
    float: glue.Schema.FLOAT,
    int: glue.Schema.INTEGER,
    Date: glue.Schema.DATE
}


def python_to_glue(a_type):
    generic_type = get_origin(a_type)
    template = list(get_args(a_type))
    if generic_type == dict:
        return glue_map(python_to_glue(template[0]), python_to_glue(template[1]))
    if generic_type == list:
        return array(python_to_glue(template[0]))
    if generic_type == Union:
        try:
            template.remove(type(None))
        except ValueError:
            ...  # no worries if it isn't in there.
    if len(template) == 1:
        return python_to_glue(template[0])

    return glue_type_map.get(a_type, glue.Schema.STRING)
