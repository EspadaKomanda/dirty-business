"""
Requests related to the auth service.
"""
from pydantic import BaseModel
from backend.app.utils.validation.pydantic_integration import Username

class LoginRequest(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for login request.
    """
    username: Username
    password: str

class RefreshTokenRequest(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for refresh token request.
    """
    refresh_token: str

class ValidateAuthTokenRequest(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for validate auth token request.
    """
    access_token: str
