"""
Object representing the user account.
"""
import peewee as pw
from .base import Base
from .user_login_data import UserLoginData
from .user_profile import UserProfile

class User(Base):
    """
    Object representing the user account.
    """
    registration_date = pw.DateTimeField()

    @classmethod
    def get_by_username(cls, username: str):
        """
        Get user by username.
        """
        return cls.get(UserLoginData.username == username)

    @classmethod
    def get_by_email(cls, email: str):
        """
        Get user by email.
        """
        return cls.get(UserLoginData.email == email)

    @property
    def login_data(self):
        """
        Property that returns the user login data.
        """
        return UserLoginData.get(user=self)

    @property
    def profile(self):
        """
        Property that returns the user profile.
        """
        return UserProfile.get(user=self)
