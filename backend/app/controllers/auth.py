"""
Controller for authentication.
"""
from fastapi_controllers import Controller, post
from backend.app.services.auth import AuthService
from backend.app.dtos.auth_service.requests import (
    RefreshTokenRequest,
    ValidateAccessTokenRequest
)
from backend.app.dtos.auth_service.responses import (
    RefreshTokenResponse,
    ValidateAccessTokenResponse
)

class AuthController(Controller):
    """Controller for authentication"""
    tags=["Auth"]

    @post("/validateAccessToken", response_model=ValidateAccessTokenResponse)
    def validate_access_token(
        self, data: ValidateAccessTokenRequest) -> ValidateAccessTokenResponse:
        """
        Validate access token.
        """
        return AuthService.validate_access_token(data.access_token)

    @post("/refreshToken", response_model=RefreshTokenResponse)
    def refresh_token(self, data: RefreshTokenRequest) -> RefreshTokenResponse:
        """
        Allows user to receive new access and refresh tokens.
        """
        return AuthService.refresh_tokens(data.refresh_token)
