"""
Object representing all the data necessary for user registration and authentication.
"""
import peewee as pw
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
    auth_token_salt = pw.CharField(min_length=36, max_length=36)
    is_email_confirmed = pw.BooleanField(default=False)
    confirmation_code = pw.CharField(null=True, min_length=6, max_length=6)
    confirmation_gen_time = pw.TimestampField(null=True)
    recovery_token = pw.CharField(null=True, unique=True, min_length=36, max_length=36)
    recovery_gen_time = pw.TimestampField(null=True)
