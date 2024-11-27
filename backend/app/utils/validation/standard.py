"""
Standard validation decorators to be used with DTOs, models and database entities.
"""
import re
from backend.app.exceptions.generic import ValidationException

# FIXME: datatype on regex
def validate_regex(field: str, regex: str, required: bool = False, message: str = None):
    """
    Validates field using the given regex. Ignores null values.
    """
    if message is None:
        message = "did not match regex."
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            value = getattr(self, field)
            if value is None and not required:
                return func(self, *args, **kwargs)
            if value is None and required:
                raise ValidationException(
                    f"{field.replace('_', ' ').capitalize()} cannot be null."
                )

            if not re.match(regex, value):
                raise ValidationException(
                    f"{field.replace('_', ' ').capitalize()} {message}"
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def validate_required(field_name):
    """
    Verifies that the given value is not empty.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            value = getattr(self, field_name)
            if not value:
                raise ValidationException(
                    f"{field_name.replace('_', ' ').capitalize()} cannot be null."
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def validate_email(field_name, required: bool = False):
    """
    Validates that a string is a valid email address.
    """
    email_regex = r'^[^@]+@[^@]+\.[a-zA-Zа-яА-Я]{2,}$'

    return validate_regex(field_name, email_regex, required, "not a valid email address.")
