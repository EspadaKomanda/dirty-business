"""
Service for working with cameras.
Designed to display the possible business-process.
"""
from fastapi import HTTPException, status
from backend.app.models.camera import Camera
from backend.app.dtos.camera_service.dtos import Camera as CameraDto
from backend.app.dtos.camera_service.responses import CamerasResponse
class CameraService:
    """
    Service for working with cameras.
    Designed to display the possible business-process.
    """
    @classmethod
    def get_camera(cls, camera_id) -> CameraDto:
        """
        Retrieve info for a particular camera.
        """
        camera = Camera.get_or_none(Camera.id == camera_id)
        if camera is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return CameraDto(**camera)

    @classmethod
    def get_cameras(cls, page=1) -> CamerasResponse:
        """
        Retrieves the first page containing 10 cameras.
        """
        camera_count = Camera.select().count()  # pylint: disable=no-value-for-parameter

        cameras: list[Camera] = list(Camera
            .select()
            .order_by(Camera.date.desc())
            .limit(10)
            .offset((int(page) - 1) * 10))

        return CamerasResponse(
            page=page,
            cameras=[CameraDto(**camera) for camera in cameras],
            total_pages=camera_count // 10
        )
