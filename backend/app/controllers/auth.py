"""
Controller for authentication.
"""
from fastapi_controllers import Controller, post
from backend.app.services.auth import AuthService
from backend.app.dtos.auth_service.requests import (
    RefreshTokenRequest
)
from backend.app.dtos.auth_service.responses import (
    RefreshTokenResponse
)

class AuthController(Controller):
    """Controller for authentication"""
    tags=["Auth"]

    @post("/refreshToken", response_model=RefreshTokenResponse)
    def refresh_token(self, data: RefreshTokenRequest) -> RefreshTokenResponse:
        """
        Allows user to receive new access and refresh tokens.
        """
        return AuthService.refresh_tokens(data.refresh_token)
