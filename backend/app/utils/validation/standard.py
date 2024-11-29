"""
Standard validation decorators to be used with DTOs, models and database entities.
"""
import re
import pendulum as pnd
from backend.app.exceptions.generic.validation_exception import ValidationException

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

def validate_guid(field_name, required: bool = False):
    """
    Validates that a string is a valid GUID.
    """
    guid_regex = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'

    return validate_regex(field_name, guid_regex, required, "not a valid GUID.")

def validate_ndigits(field_name, digits: int, required: bool = False):
    """
    Validates that a string is a valid ndigit code.
    """
    code_regex = f'^[0-9]{{{digits}}}$'

    return validate_regex(field_name, code_regex, required, "not a valid code.")

def validate_url(field_name, domain: str = None, path: str = None, required: bool = False):
    """
    Validates that a string is a valid URL.
    """
    url_regex = r"""^(?!.*\.\.)(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w.-]+)+[\w\-._~:/?#[\]@!\$&'$$\*\+,;=.]+$"""  # pylint: disable=line-too-long

    if domain is not None and path is not None:
        url_regex = f'^{domain}\/{path}'

    return validate_regex(field_name, url_regex, required, "not a valid URL.")

def validate_date_before(field_name, before_date: pnd.datetime, required: bool = False):
    """
    Validates that a date is before before_date.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            value = getattr(self, field_name)
            if value is None and not required:
                return func(self, *args, **kwargs)
            if value is None and required:
                raise ValidationException(
                    f"{field_name.replace('_', ' ').capitalize()} cannot be null."
                )

            if value > before_date:
                raise ValidationException(
                    f"{field_name.replace('_', ' ').capitalize()} must be before {before_date}."
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def validate_date_after(field_name, after_date: pnd.datetime, required: bool = False):
    """
    Validates that a date is after after_date.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            value = getattr(self, field_name)
            if value is None and not required:
                return func(self, *args, **kwargs)
            if value is None and required:
                raise ValidationException(
                    f"{field_name.replace('_', ' ').capitalize()} cannot be null."
                )

            if value < after_date:
                raise ValidationException(
                    f"{field_name.replace('_', ' ').capitalize()} must be after {after_date}."
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def validate_date_between(
    field_name,
    start_date: pnd.datetime,
    end_date: pnd.datetime,
    required: bool = False
    ):
    """
    Validates that a date is between start_date and end_date.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            value = getattr(self, field_name)
            if value is None and not required:
                return func(self, *args, **kwargs)
            if value is None and required:
                raise ValidationException(
                    f"{field_name.replace('_', ' ').capitalize()} cannot be null."
                )

            if value < start_date or value > end_date:
                raise ValidationException(
                    f"{field_name.replace('_', ' ').capitalize()} "
                    "must be between {start_date} and {end_date}."
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
