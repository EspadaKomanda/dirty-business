"""
Data transfer objects for auth service.
"""
from datetime import datetime
from pydantic import BaseModel

class TokenData(BaseModel):
    """
    Data transfer object for token data.
    role: the name of the user's role\n
    token_type: the type of token (access or refresh)\n
    salt: user's session salt\n
    """
    user_id: int | str
    username: str
    role: str
    token_type: str
    salt: str
    exp: datetime | str
    iss: str
    aud: str

class UserAccount(BaseModel):
    """
    Data transfer object for user account.
    """
    id: int
    username: str
    role: str
    salt: str | None
