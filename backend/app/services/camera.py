"""
Service for working with cameras.
Designed to display the possible business-process.
"""
from backend.app.dtos.camera_service.dtos import Camera
from backend.app.dtos.camera_service.responses import CamerasResponse
class CameraService:
    """
    Service for working with cameras.
    Designed to display the possible business-process.
    """
    @classmethod
    def get_camera(cls, camera_id) -> Camera:
        """
        Retrieve info for a particular camera.
        """
        raise NotImplementedError

    @classmethod
    def get_cameras(cls, page=1) -> CamerasResponse:
        """
        Retrieves the first page containing 10 cameras.
        """
        raise NotImplementedError
