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

class ValidateAuthTokenResponse(BaseModel):
    """
    Data transfer object for login request.
    """
    is_valid: bool

class LoginResponse(RefreshTokenResponse):
    """
    Data transfer object for login request.
    """
