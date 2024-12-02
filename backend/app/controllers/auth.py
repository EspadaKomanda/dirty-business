"""
Controller for authentication.
"""
from fastapi_controllers import Controller, post
from backend.app.dtos.auth_service.requests import (
    LoginRequest,
    RefreshTokenRequest,
    ValidateAuthTokenRequest
)
from backend.app.dtos.auth_service.responses import (
    LoginResponse,
    RefreshTokenResponse,
    ValidateAuthTokenResponse
)

class AuthController(Controller):
    """Controller for authentication"""
    tags=["Auth"]

    @post("/login", response_model=LoginResponse)
    def login(self, data: LoginRequest) -> LoginResponse:
        """
        Allows user to login using their username and password.
        """
        return LoginResponse(test=str(data))

    @post("/refreshToken", response_model=RefreshTokenResponse)
    def refresh_token(self, data: RefreshTokenRequest) -> RefreshTokenResponse:
        """
        Allows user to receive new access and refresh tokens.
        """
        return RefreshTokenResponse(test=str(data))

    @post("/validateAuthToken", response_model=ValidateAuthTokenResponse)
    def validate_auth_token(self, data: ValidateAuthTokenRequest) -> ValidateAuthTokenResponse:
        """
        Validates auth token.
        """
        return ValidateAuthTokenResponse(test=str(data))
