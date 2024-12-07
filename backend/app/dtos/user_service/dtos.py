"""
UserService DTOs.
"""
from pydantic import BaseModel

class UserProfile(BaseModel):
    """
    Dto representing the user profile.
    """
    name: str
    surname: str
    patronymic: str | None = None
    avatar_url: str | None
