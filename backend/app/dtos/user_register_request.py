"""
Data transfer object for user registration request.
"""

from pydantic import EmailStr
from backend.app.utils.validation.username import validate_username
from .base import BaseDto

class UserRegisterRequest(BaseDto):
    """
    Data transfer object for user registration request.
    """
    username:  str
    email: EmailStr
    password: str

    @validate_username("username", required=True)
    def clean(self):
        return self
