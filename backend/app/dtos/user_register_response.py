"""
Data transfer object for user registration response.
"""
from pydantic import BaseModel

class UserRegisterResponse(BaseModel):
    """
    Data transfer object for user registration response.
    """
    test: str
