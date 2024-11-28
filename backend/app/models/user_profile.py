"""
Object representing the user profile.
"""
import peewee as pw
from app.utils.validation.name import validate_name
from .base import Base
from .user import User

class UserProfile(Base):
    """
    Object representing the user profile.
    """
    user = pw.ForeignKeyField(User, backref="user_profile", on_delete="CASCADE")
    name = pw.CharField(max_length=100)
    surname = pw.CharField(max_length=100)
    patronymic = pw.CharField(null=True, max_length=100)
    avatar_url = pw.CharField(null=True, max_length=100)

    @validate_name("name", required=True)
    @validate_name("surname", required=True)
    @validate_name("patronymic")
    def clean(self):
        """validation"""
