"""Controller for operations with users."""
import json
from fastapi import Response, status
from fastapi_controllers import Controller, get

class UserController(Controller):
    """Controller for operations with users."""
    tags=["Users"]

    @get("/user/{user_id}", response_class=Response)
    async def get_user_object(self, user_id: int) -> Response:
        """Get user object."""
        return Response(
            content=json.dumps({"user_id": user_id}),
            status_code=status.HTTP_200_OK,
            media_type="application/json"
        )
