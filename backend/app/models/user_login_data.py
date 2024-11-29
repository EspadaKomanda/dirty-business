"""
Object representing all the data necessary for user registration and authentication.
"""
import peewee as pw
from backend.app.utils.sanitization.standard import sanitize_all
from backend.app.utils.validation.username import validate_username
from backend.app.utils.validation.standard import (
    validate_email,
    validate_guid,
    validate_ndigits
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
    auth_token_salt = pw.CharField(max_length=36)
    is_email_confirmed = pw.BooleanField(default=False)
    confirmation_code = pw.CharField(null=True, max_length=6)
    confirmation_gen_time = pw.TimestampField(null=True)
    recovery_token = pw.CharField(null=True, unique=True, max_length=36)
    recovery_gen_time = pw.TimestampField(null=True)

    @sanitize_all()
    @validate_username("username", required=True)
    @validate_email("email", required=True)
    @validate_guid("auth_token_salt")
    @validate_guid("recovery_token")
    @validate_ndigits("confirmation_code", 6)
    def clean(self):
        """validation"""
        return self
