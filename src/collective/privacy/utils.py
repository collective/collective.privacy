# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from six import text_type, binary_type

import re
import sys


def match_string(expr, str):
    """
    Checks if expression matches provided string, supporting wildcard (*)
    Ex: foo* matches foobar
    """
    expr = "^{}$".format(expr)
    return bool(re.match(expr.replace("*", ".*"), str))


def safe_fieldname(text):
    """
    This function ensure that the name of a generated field is comptabible with
    the current python version
    str for python 2
    str for python 3
    """
    if sys.version_info[0] > 2:
        if not isinstance(text, text_type):
            return safe_unicode(text)
    else:
        if not isinstance(text, binary_type):
            return str(text)
    return text
