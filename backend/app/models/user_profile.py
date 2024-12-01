"""
Object representing the user profile.
"""
import peewee as pw
from backend.app.utils.validation.name import v_name
from backend.app.utils.validation.standard import validate_field, v_url
from .base import Base
from .user import User

class UserProfile(Base):
    """
    Object representing the user profile.
    """
    user = pw.ForeignKeyField(
        User,
        null=False,
        backref="user_profile",
        on_delete="CASCADE"
    )

    name = pw.CharField(max_length=100)

    surname = pw.CharField(max_length=100)

    patronymic = pw.CharField(null=True, max_length=100)

    avatar_url = pw.CharField(null=True, max_length=100)

    def validate(self):
        """
        Function to run validation on.
        """
        validate_field(self, "name", v_name)
        validate_field(self, "surname", v_name)
        validate_field(self, "patronymic", v_name)
        validate_field(self, "avatar_url", v_url)
        return self
