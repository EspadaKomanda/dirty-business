"""
Object representing all the data necessary for user registration and authentication.
"""
import peewee as pw
from backend.app.utils.validation.standard import (
    validate_field,
    v_email,
    v_guid,
)
from backend.app.utils.validation.special import (
    v_username,
    v_registration_code
)

from .base import Base
from .user import User

class UserLoginData(Base):
    """
    Object representing all the data necessary for user registration and authentication.
    """
    user = pw.ForeignKeyField(User, backref="user_login_data", on_delete="CASCADE")

    username = pw.CharField(unique=True, max_length=18)

    email = pw.CharField(unique=True, max_length=50)

    password_hash = pw.CharField(max_length=60)

    auth_token_salt = pw.CharField(null=True, max_length=36)

    is_email_confirmed = pw.BooleanField(default=False)

    confirmation_code = pw.CharField(null=True, max_length=6)

    confirmation_gen_time = pw.TimestampField(null=True)

    recovery_token = pw.CharField(null=True, unique=True, max_length=36)

    recovery_gen_time = pw.TimestampField(null=True)

    def validate(self):
        """
        Function to run validation on.
        """
        validate_field(self, "username", v_username)
        validate_field(self, "email", v_email)
        validate_field(self, "auth_token_salt", v_guid)
        validate_field(self, "confirmation_code", v_registration_code)
        validate_field(self, "recovery_token", v_guid)

        return self
