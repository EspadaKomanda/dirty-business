"""
Object representing the user profile.
"""
import peewee as pw
from .base import Base
from .user import User

class UserProfile(Base):
    """
    Object representing the user profile.
    """
    user = pw.ForeignKeyField(User, backref="profiles", on_delete="CASCADE")
    name = pw.CharField(max_length=100)
    surname = pw.CharField(max_length=100)
    patronymic = pw.CharField(null=True, max_length=100)
    avatar_url = pw.CharField(null=True, max_length=100)
