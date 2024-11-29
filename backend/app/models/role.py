"""
Object representing a role.
"""
import peewee as pw
from backend.app.utils.sanitization.standard import sanitize_all
from backend.app.utils.validation.standard import validate_length
from .base import Base

class Role(Base):
    """
    Object representing a role.
    """
    name = pw.CharField(max_length=18, unique=True)

    @sanitize_all()
    @validate_length("name", min_length=3, max_length=18)
    def clean(self):
        """validation"""
        return self
