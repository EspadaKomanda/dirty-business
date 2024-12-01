"""
Data transfer object for user registration request.
"""

from pydantic import BaseModel, EmailStr, validator
from backend.app.utils.validation.standard import v_email
from backend.app.utils.validation.username import v_username
from backend.app.utils.validation.password import v_password

class UserRegisterRequest(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for user registration request.
    """
    username:  str
    email: EmailStr
    password: str

    @validator('username')
    @classmethod
    def validate_username(cls, value: str):
        """
        Validates username.
        """
        if not v_username(value):
            raise ValueError("Invalid username.")

        return value

    @validator('email')
    @classmethod
    def validate_email(cls, value: str):
        """
        Validates email.
        """
        if not v_email(value):
            raise ValueError("Invalid email.")

        return value

    @validator('password')
    @classmethod
    def validate_password(cls, value: str):
        """
        Validates password.
        """
        if not v_password(value):
            raise ValueError("Insufficiently strong password.")

        return value
