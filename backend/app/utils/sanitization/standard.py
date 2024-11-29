"""
Standard set of decorators for value sanitization in data models.
"""
def sanitize_all(exclude: list = None):
    """
    Sanitizes all values in the model by trimming leading and trailing spaces.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            for field_name in self.__dict__:

                if exclude is not None and field_name not in exclude:  # Ignore excluded
                    value = getattr(self, field_name)

                    if value is None:
                        continue

                    # Strip spaces
                    setattr(self, field_name, value.strip())

            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def sanitize_trim(field_name):
    """
    Sanitizes the given value by trimming leading and trailing spaces.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            value = getattr(self, field_name)

            # Ignore null
            if value is None:
                return func(self, *args, **kwargs)

            # Strip spaces
            setattr(self, field_name, value.strip())

            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def sanitize_lower(field_name):
    """
    Sanitizes the given value by converting it to lowercase.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            value = getattr(self, field_name)
            if value is None:
                return func(self, *args, **kwargs)
            setattr(self, field_name, value.lower())
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def sanitize_upper(field_name):
    """
    Sanitizes the given value by converting it to uppercase.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            value = getattr(self, field_name)
            if value is None:
                return func(self, *args, **kwargs)
            setattr(self, field_name, value.upper())
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def sanitize_capitalize(field_name):
    """
    Sanitizes the given value by converting it to title case.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            value = getattr(self, field_name)
            if value is None:
                return func(self, *args, **kwargs)
            setattr(self, field_name, value.title())
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
