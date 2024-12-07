"""
Controller for operations with cameras.
"""
import logging
from typing import Annotated
from fastapi_controllers import Controller, get
from fastapi import Depends
from backend.app.dtos.auth_service.dtos import UserAccount
from backend.app.services.auth import AuthService
from backend.app.services.camera import CameraService
from backend.app.dtos.camera_service.dtos import Camera
from backend.app.dtos.camera_service.responses import CamerasResponse

logger = logging.getLogger(__name__)

class CameraController(Controller):
    """Controller for operations with cameras."""
    tags=["Camera"]

    @get("/cameras", response_model=CamerasResponse)
    def get_cameras(self,
        user: Annotated[UserAccount, Depends(AuthService.authenticate)]) -> CamerasResponse:
        """
        Retrieves the first page containing 10 cameras.
        Includes the total number of pages.
        """
        logger.info("User %s is retrieving cameras", user.username)
        return CameraService.get_cameras()

    @get("/cameras/{camera_id}", response_model=Camera)
    def get_camera(self, camera_id,
        user: Annotated[UserAccount, Depends(AuthService.authenticate)]) -> Camera:
        """
        Retrieve info for a particular camera.
        """
        logger.info("User %s is retrieving camera %s", user.username, camera_id)
        return CameraService.get_camera(camera_id)

    @get("/cameras/pages/{page}", response_model=CamerasResponse)
    def get_cameras_page(self, page,
        user: Annotated[UserAccount, Depends(AuthService.authenticate)]) -> CamerasResponse:
        """
        Retrieves a certain page of cameras.
        """
        logger.info("User %s is retrieving cameras page %s", user.username, page)
        return CameraService.get_cameras(page)
