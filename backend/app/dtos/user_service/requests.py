"""
Requests related to the user service.
"""
from pydantic import BaseModel, EmailStr, FileUrl

from backend.app.utils.validation.pydantic_integration import (
    Name,
    Password,
    Username,
    RegistrationCode
)

class BeginRegistrationRequest(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for user registration request.

    Username must be unique and have between 3 and 18 characters.
    Only Latin characters, numbers, and underscores are allowed.

    Password must be 8-50 characters long, contain at least one lowercase and one uppercase letter,
    at least one digit, at least one special character, and not contain whitespace characters.
    Only Latin characters are allowed.
    """
    email: EmailStr
    username: Username
    password: Password

class CheckRegistrationCodeRequest(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for user registration confirmation request.

    Confirmation code must be 6 digits and not expired.
    """
    email: EmailStr
    confirmation_code: RegistrationCode

class CompleteRegistrationRequest(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for user registration completion request.

    Confirmation code must be 6 digits and not expired.

    Name, surname and patronymic must be between 1 and 100 characters.
    """
    email: EmailStr
    confirmation_code: RegistrationCode
    name: Name
    surname: Name
    patronymic: Name | None = None
    avatar_url: FileUrl | None = None
