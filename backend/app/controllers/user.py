"""
Controller for user actions.
"""
from fastapi_controllers import Controller, post
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
from backend.app.services.user import UserService

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
