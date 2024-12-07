"""
Responses related to the camera service.
"""
from pydantic import BaseModel

from .dtos import Camera

class CamerasResponse(BaseModel):
    """
    Response for retrieving a page of cameras.\n
    page - the current page number;\n
    cameras - the list of cameras on the page (up to 10);\n
    total_pages - the total number of existing pages\n
    """
    page: int
    cameras: list[Camera]
    total_pages: int
