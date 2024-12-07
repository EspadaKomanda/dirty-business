"""
Data transfer objects for camera object.
"""
from datetime import datetime
from pydantic import BaseModel

class Camera(BaseModel):
    """
    Data transfer object for camera object.\n
    id - id of the camera;\n
    name - camera name;\n
    contamination - contamination percentage;\n
    date - date when last photo was captured;\n
    url - url to the photo;\n
    """
    id: int
    name: str
    description: str | None
    contamination: float
    date: datetime
    url: str | None
