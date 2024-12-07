"""
Object representing a camera.
"""

import peewee as pw
from backend.app.utils.validation.standard import validate_field, v_url
from .base import Base

class Camera(Base):
    """
    Object representing a camera.
    """
    name = pw.CharField(max_length=100, unique=True)

    description = pw.CharField(null=True, max_length=500)

    date = pw.DateTimeField()

    url = pw.CharField(null=True, max_length=100)

    def validate(self):
        """
        Function to run validation on.
        """
        validate_field(self, "name", v_url)
        validate_field(self, "url", v_url)
        return self
