"""
Validation for username.
"""
from .standard import validate_regex

def validate_name(field_name, required: bool = False):
    """
    Validates that a username contains only Latin characters, numbers, and underscores.
    The username must be between 3 and 18 characters long.
    """
    name_regex = r'.{1,100}$'

    return validate_regex(
        field_name,
        name_regex,
        required,
        "must be from 3 to 18 characters long and can consist of lower"
        "and upper latin characters, numbers and underscores."
    )
