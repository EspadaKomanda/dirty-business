"""
Service for authenticating users.
"""
import logging
import jwt
import pendulum as pnd
import pydantic as pyd
import peewee as pw
from fastapi import HTTPException, status
from backend.app.config import (
    JWT_KEY,
    JWT_ACCESS_EXPIRE_MINUTES,
    JWT_REFRESH_EXPIRE_MINUTES,
    JWT_ISSUER,
    JWT_AUDIENCE,
    JWT_ALGORITHM
)
from backend.app.models.user import User
from backend.app.models.user_login_data import UserLoginData
from backend.app.models.user_role import UserRole
from backend.app.models.role import Role
from backend.app.dtos.auth_service.dtos import TokenData
from backend.app.dtos.auth_service.responses import (
    RefreshTokenResponse,
    ValidateAccessTokenResponse
)

logger = logging.getLogger(__name__)

class AuthService:
    """
    Service for authenticating users.
    """
    @classmethod
    def _generate_token(cls, user_id: str, token_type: str) -> str:
        user: User
        user_login_data: UserLoginData
        role: Role
        try:
            user = User.get_by_id(user_id)
        except pw.DataError:
            logger.error("Attempted to generate token for non-existent user")
            raise

        try:
            user_login_data = UserLoginData.get(user=user)
        except pw.DataError:
            logger.error("Login data for user %s not found", user_id)
            raise

        try:
            role = Role.get_by_id(UserRole.get(user=user).role)

        except pw.DataError:
            logger.error("Role for user %s not found", user_id)
            raise

        encoded_jwt: str
        try:
            exipre = pnd.now()
            if token_type == "access":
                exipre += pnd.duration(minutes=int(JWT_ACCESS_EXPIRE_MINUTES))
            elif token_type == "refresh":
                exipre += pnd.duration(minutes=int(JWT_REFRESH_EXPIRE_MINUTES))

            data = TokenData(
                user_id=user.id,
                username=user_login_data.username,
                role=role.name,
                token_type=token_type,
                salt=user_login_data.auth_token_salt,
                exp=exipre,
                iss=JWT_ISSUER,
                aud=JWT_AUDIENCE
            ).dict()

            encoded_jwt = jwt.encode(data, JWT_KEY, algorithm=JWT_ALGORITHM)

        except Exception:
            logger.error("Failed generating token for user %s ", user_id)
            raise

        return encoded_jwt

    @classmethod
    def _validate_token(cls, token: str, token_type: str) -> User:
        # TODO: implement caching

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode token and parse data as TokenData object
            data = TokenData(**jwt.decode(
                token,
                key=JWT_KEY,
                algorithms=[JWT_ALGORITHM],
                audience=JWT_AUDIENCE,
                issuer=JWT_ISSUER
                ))

            user = User.get_by_id(data.user_id)
            user_login_data = UserLoginData.get(user=user)

            # Validate salt
            if user_login_data.auth_token_salt != data.salt:
                raise credentials_exception

            # Validate token type
            if data.token_type != token_type:
                raise credentials_exception

            return user

        # TODO: review exception handling on FastAPI side
        except pyd.ValidationError as e:
            logger.error("Token serialization failed: %s", e)
            raise credentials_exception from e
        except jwt.InvalidTokenError as e:
            logger.warning("Token is invalid: %s", e)
            raise credentials_exception from e
        except pw.DataError as e:
            logger.error("Could not find user: %s", e)
            raise credentials_exception from e
        except Exception as e:
            logger.error("Token validation failed: %s", e)
            raise e

    @classmethod
    def generate_access_token(cls, user_id: str) -> str:
        """
        Generate access token for user.
        """
        return cls._generate_token(user_id, "access")

    @classmethod
    def generate_refresh_token(cls, user_id: str) -> str:
        """
        Generate refresh token for user.
        """
        return cls._generate_token(user_id, "refresh")

    @classmethod
    def validate_access_token(cls, access_token: str) -> ValidateAccessTokenResponse:
        """
        Validate token.
        """
        user = cls._validate_token(access_token, "access")

        return ValidateAccessTokenResponse(
            is_valid=user is not None
        )


    @classmethod
    def refresh_tokens(cls, refresh_token: str) -> RefreshTokenResponse:
        """
        Generates and returns access & refresh token if refresh token is still valid.
        """
        user = cls._validate_token(refresh_token, "refresh")
        if user is None:
            raise RuntimeError("Could not validate token")

        access_token = cls._generate_token(user, "access")
        refresh_token = cls._generate_token(user, "refresh")
        return RefreshTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
