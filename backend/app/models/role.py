"""
Object representing a role.
"""
import peewee as pw
from backend.app.utils.validation.standard import validate_field, v_length
from .base import Base

class Role(Base):
    """
    Object representing a role.
    """
    name = pw.CharField(max_length=18, unique=True)

    def validate(self):
        """
        Function to run validation on.
        """
        validate_field(self, "name",  v_length, min_length=3, max_length=18)
        return self
