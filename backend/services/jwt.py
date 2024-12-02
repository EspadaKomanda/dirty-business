"""
Service for generating, decoding and validating JWT tokens.
"""
from backend.app.config import (
    JWT_KEY,
    JWT_ACCESS_EXPIRE_MINUTES,
    JWT_REFRESH_EXPIRE_MINUTES,
    JWT_ISSUER,
    JWT_AUDIENCE
)
from backend.app.models.user import User

class JwtService:
    """
    Service for generating, decoding and validating JWT tokens.
    """

    @classmethod
    def _generate_token(cls, user_id: str, token_type: str) -> str:
        # TODO: implement
        return ""

    @classmethod
    def _decode_token(cls, token: str) -> dict:
        # TODO: implement
        return {}

    @classmethod
    def generate_access_token(cls, user_id: str) -> str:
        """
        Generate access token.
        """
        return cls._generate_token(user_id, "access")

    @classmethod
    def generate_refresh_token(cls, user_id: str) -> str:
        """
        Generate refresh token.
        """
        return cls._generate_token(user_id, "refresh")

    @classmethod
    def validate_access_token(cls, access_token: str) -> User:
        """
        Validate token.
        """
        # TODO: implement
        return None

    @classmethod
    def refresh_tokens(cls, refresh_token: str) -> User:
        """
        Validate token.
        """
        # TODO: implement
        return None
