"""
Controller for operations with users.
"""
from fastapi_controllers import Controller, get, post
from backend.app.dtos.user_register_request import UserRegisterRequest
from backend.app.dtos.user_register_response import UserRegisterResponse

class UserController(Controller):
    """Controller for operations with users."""
    tags=["Users"]

    @get("/user/{user_id}")
    async def get_user_object(self, user_id: int) -> UserRegisterRequest:
        """Get user object."""
        return UserRegisterRequest(
            username=str(user_id),
            email="email@email.com",
            password="password"
        )

    @post("/user", response_model=UserRegisterResponse)
    def register_user(self, data: UserRegisterRequest) -> UserRegisterResponse:
        """Register user."""
        return UserRegisterResponse(test=str(data))
