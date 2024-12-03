"""
Responses related to the user service.
"""
from pydantic import BaseModel
from backend.app.dtos.auth_service.responses import RefreshTokenResponse

class BeginRegistrationResponse(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for user registration response.
    """
    success: bool

class CheckRegistrationCodeResponse(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for user registration confirmation response.
    """
    success: bool

class CompleteRegistrationResponse(RefreshTokenResponse):
    """
    Data transfer object for user registration completion response.
    Contains access and refresh tokens.
    """
