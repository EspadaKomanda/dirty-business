"""
Validation for username.
"""
from .standard import validate_regex

def validate_username(field_name, required: bool = False):
    """
    Validates that a username contains only Latin characters, numbers, and underscores.
    The username must be between 3 and 18 characters long.
    """
    username_regex = r'^[a-zA-Z0-9_]{3,18}$'

    return validate_regex(
        field_name,
        username_regex,
        required,
        "must be from 3 to 18 characters long and can consist of lower"
        "and upper latin characters, numbers and underscores.")
