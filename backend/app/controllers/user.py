"""
Controller for operations with users.
"""
from fastapi_controllers import Controller, get, post
from backend.app.dtos.user_service.requests import UserRegisterRequest
from backend.app.dtos.user_service.responses import UserRegisterResponse

class UserController(Controller):
    """Controller for operations with users."""
    tags=["Users"]

    @get("/user/{user_id}")
    async def get_user_object(self, user_id: int) -> UserRegisterRequest:
        """
        Retrieve user object.
        """
        return UserRegisterRequest(
            username=str(user_id),
            email="email@email.com",
            password="password"
        )

    @post("/user", response_model=UserRegisterResponse)
    def register_user(self, data: UserRegisterRequest) -> UserRegisterResponse:
        """Register user."""
        return UserRegisterResponse(test=str(data))

    @get("/greetMe/{user_id}")
    async def greet_me(self, user_id: int) -> str:
        """Greet user."""
        return f"Hello, {user_id}"
