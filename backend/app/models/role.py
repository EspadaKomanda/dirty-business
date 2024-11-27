"""
Object representing a role.
"""
import peewee as pw
from .base import Base

class Role(Base):
    """
    Object representing a role.
    """
    name = pw.CharField(max_length=18, unique=True)
