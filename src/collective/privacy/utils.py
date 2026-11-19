from plone.base.utils import safe_text

import re


def match_string(expr, str):
    """
    Checks if expression matches provided string, supporting wildcard (*)
    Ex: foo* matches foobar
    """
    expr = f"^{expr}$"
    return bool(re.match(expr.replace("*", ".*"), str))


def safe_fieldname(text):
    """Return the name of a generated field as text."""
    return safe_text(text)
