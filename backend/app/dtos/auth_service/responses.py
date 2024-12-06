"""
Requests related to the auth service.
"""
from pydantic import BaseModel

class RefreshTokenResponse(BaseModel):
    """
    Data transfer object for login request.
    """
    access_token: str
    refresh_token: str

class ValidateAccessTokenResponse(BaseModel):
    """
    Data transfer object for login request.
    An error is returned if token is invalid.
    """
    is_valid: bool

class LoginResponse(RefreshTokenResponse):
    """
    Data transfer object for login request.
    """
