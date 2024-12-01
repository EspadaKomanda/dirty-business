"""
Validates that a string is a valid username.
"""
import re

def v_username(value: str):
    """
    Validates that a username contains only Latin characters, numbers, and underscores.
    The username must be between 3 and 18 characters long.
    """
    username_regex = r'^[a-zA-Z0-9_]{3,18}$'

    return re.match(username_regex, value)
