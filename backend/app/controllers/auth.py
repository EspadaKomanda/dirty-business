"""
Controller for authentication.
"""

from fastapi_controllers import Controller, post
from backend.app.services.auth import AuthService
from backend.app.dtos.auth_service.requests import (
    RefreshTokenRequest,
    ValidateAccessTokenRequest,
    LoginRequest
)
from backend.app.dtos.auth_service.responses import (
    RefreshTokenResponse,
    ValidateAccessTokenResponse,
    LoginResponse
)

class AuthController(Controller):
    """Controller for authentication"""
    tags=["Auth"]

    @post("/login", response_model=LoginResponse)
    def login(self, data: LoginRequest, ) -> LoginResponse:
        """
        Allows user to login.
        """
        return AuthService.login(data)

    @post("/validateAccessToken", response_model=ValidateAccessTokenResponse)
    def validate_access_token(
        self, data: ValidateAccessTokenRequest) -> ValidateAccessTokenResponse:
        """
        Validate access token.
        """
        return AuthService.validate_access_token(data)

    @post("/refreshToken", response_model=RefreshTokenResponse)
    def refresh_token(self, data: RefreshTokenRequest) -> RefreshTokenResponse:
        """
        Allows user to receive new access and refresh tokens.
        """
        return AuthService.refresh_tokens(data)
