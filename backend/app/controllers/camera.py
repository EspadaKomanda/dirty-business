"""
Controller for operations with cameras.
"""
from fastapi_controllers import Controller, get
from backend.app.services.camera import CameraService
from backend.app.dtos.camera_service.dtos import Camera
from backend.app.dtos.camera_service.responses import CamerasResponse

class CameraController(Controller):
    """Controller for operations with cameras."""
    tags=["Camera"]

    @get("/cameras", response_model=CamerasResponse)
    def get_cameras(self) -> CamerasResponse:
        """
        Retrieves the first page containing 10 cameras.
        Includes the total number of pages.
        """
        return CameraService.get_cameras()

    @get("/cameras/{camera_id}", response_model=Camera)
    def get_camera(self, camera_id) -> Camera:
        """
        Retrieve info for a particular camera.
        """
        return CameraService.get_camera(camera_id)

    @get("/cameras/pages/{page}", response_model=CamerasResponse)
    def get_cameras_page(self, page) -> CamerasResponse:
        """
        Retrieves a certain page of cameras.
        """
        return CameraService.get_cameras(page)
