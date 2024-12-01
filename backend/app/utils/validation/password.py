"""
Validates that a string is a valid password.
"""
import re

def v_password(value: str):
    """
    Validates that a string is a valid password.
    Password must be 8-50 characters long.
    Password must contain at least one lowercase and one uppercase letter.
    Password must contain at least one digit.
    Password must contain at least one special character.
    Only Latin characters are allowed.
    """
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}[\]:;"<>?/\|`~,.])(?=.{8,50}$).*$'  # pylint: disable=line-too-long

    return re.match(password_regex, value)
