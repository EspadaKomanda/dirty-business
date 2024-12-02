"""
Data transfer objects for auth service.
"""
import pendulum as pnd
from pydantic import BaseModel

class TokenData(BaseModel):
    """
    Data transfer object for token data.
    role: the name of the user's role\n
    token_type: the type of token (access or refresh)\n
    salt: user's session salt\n
    """
    user_id: str
    username: str
    role: str
    token_type: str
    salt: str
    exp: pnd.DateTime
    iss: str
    aud: str
