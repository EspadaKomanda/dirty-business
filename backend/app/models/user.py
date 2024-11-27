"""
Object representing the user account.
"""
import peewee as pw
from .base import Base

class User(Base):
    """
    Object representing the user account.
    """
    registration_date = pw.DateTimeField()