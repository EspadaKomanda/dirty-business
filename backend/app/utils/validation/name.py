"""
Validation for name.
"""
from .standard import validate_regex

def validate_name(field_name, required: bool = False):
    """
    Validates name.
    """
    name_regex = r'.{1,100}$'

    return validate_regex(
        field_name,
        name_regex,
        required,
        "name cannot be longer than 100 characters."
    )
