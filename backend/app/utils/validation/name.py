"""
Validates that a string is a valid name.
"""
import re

def v_name(value: str):
    """
    Validates that a string is a valid name.
    """
    name_regex = r'.{1,100}$'

    return re.match(name_regex, value)
