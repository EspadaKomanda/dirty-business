"""
Controller for user actions.
"""
from typing import Annotated
from fastapi_controllers import Controller, get, post
from fastapi import Depends
from backend.app.dtos.auth_service.dtos import UserAccount
from backend.app.dtos.user_service.requests import (
    BeginRegistrationRequest,
    CheckRegistrationCodeRequest,
    CompleteRegistrationRequest
)
from backend.app.dtos.user_service.responses import (
    BeginRegistrationResponse,
    CheckRegistrationCodeResponse,
    CompleteRegistrationResponse
)
from backend.app.dtos.user_service.dtos import UserProfile
from backend.app.services.user import UserService
from backend.app.services.auth import AuthService

class UserController(Controller):
    """Controller for operations with users."""
    tags=["Users"]

    @post("/beginRegistration", response_model=BeginRegistrationResponse)
    def begin_user_registration(
        self, data: BeginRegistrationRequest) -> BeginRegistrationResponse:
        """Register user."""
        return UserService.begin_registration(data)

    @post("/checkRegistrationCode", response_model=CheckRegistrationCodeResponse)
    def check_user_registration_code(
        self, data: CheckRegistrationCodeRequest) -> CheckRegistrationCodeResponse:
        """Verify that registration code is valid."""
        return UserService.check_registration_code(data)

    @post("/completeRegistration", response_model=CompleteRegistrationResponse)
    def complete_user_registration(
        self, data: CompleteRegistrationRequest) -> CompleteRegistrationResponse:
        """Register user."""
        return UserService.complete_registration(data)

    @get("/profile", response_model=UserProfile)
    def get_user_profile(self,
        user: Annotated[UserAccount, Depends(AuthService.authenticate)]) -> UserProfile:
        """Get user profile."""
        return UserService.get_user_profile(user.user_id)
