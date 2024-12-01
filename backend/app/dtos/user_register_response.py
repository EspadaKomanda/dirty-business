"""
Data transfer object for user registration response.
"""
from pydantic import BaseModel

class UserRegisterResponse(BaseModel, str_strip_whitespace=True):
    """
    Data transfer object for user registration response.
    """
    test: str
