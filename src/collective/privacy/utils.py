# -*- coding: utf-8 -*-
import re


def match_string(expr, str):
    """
    Checks if expression matches provided string, supporting wildcard (*)
    Ex: foo* matches foobar
    """
    expr = "^{}$".format(expr)
    return bool(re.match(expr.replace("*", ".*"), str))
