"""
Service for authenticating users.
"""
import json
import logging
import jwt
import pendulum as pnd
import pydantic as pyd
import peewee as pw
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
from backend.app.dtos.auth_service.dtos import TokenData, UserAccount
from backend.app.dtos.auth_service.requests import (
    ValidateAccessTokenRequest,
    RefreshTokenRequest,
    LoginRequest
)
from backend.app.dtos.auth_service.responses import (
    RefreshTokenResponse,
    ValidateAccessTokenResponse,
    LoginResponse
)
from backend.app.utils.security.hashing import verify_password
from backend.app.services.redis import RedisService as redis

logger = logging.getLogger(__name__)

http_bearer_scheme = HTTPBearer()

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
    def _validate_token(cls, token: str, token_type: str) -> UserAccount:

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

            account: UserAccount

            # Add user to Redis if it is not there yet
            if not redis.exists(f"user:{data.user_id}"):
                user = User.get_by_id(data.user_id)

                account = UserAccount(
                    id=user.id,
                    username=user.login_data.username,
                    role=user.role,
                    salt=user.login_data.auth_token_salt
                )
                redis.set(f"user:{data.user_id}", account.json())

            # Get user from Redis
            redis_user = json.loads(redis.get(f"user:{data.user_id}"))
            print(redis_user)
            account = UserAccount(**redis_user)

            # Validate salt
            if account.salt != data.salt:
                raise credentials_exception

            # Validate token type
            if data.token_type != token_type:
                raise credentials_exception

            return account

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
    def validate_access_token(
        cls, request: ValidateAccessTokenRequest) -> ValidateAccessTokenResponse:
        """
        Validate token.
        """
        user = cls._validate_token(request.access_token, "access")

        return ValidateAccessTokenResponse(
            is_valid=user is not None
        )

    @classmethod
    def refresh_tokens(cls, request: RefreshTokenRequest) -> RefreshTokenResponse:
        """
        Generates and returns access & refresh token if refresh token is still valid.
        """
        user = cls._validate_token(request.refresh_token, "refresh")
        if user is None:
            raise RuntimeError("Could not validate token")

        access_token = cls.generate_access_token(user)
        refresh_token = cls.generate_refresh_token(user)
        return RefreshTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @classmethod
    def login(cls, request=LoginRequest) -> LoginResponse:
        """
        Validate user credentials and return access token.
        """
        user: User
        user_login_data: UserLoginData
        try:
            user = User.get_by_username(request.username)
            user_login_data = UserLoginData.get(user=user)
        except Exception as e:
            logger.warning(
                "Attempt to login in to user %s that was not found: %s"
                , request.username, e
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            ) from e

        if (not user_login_data.is_email_confirmed or
            not verify_password(request.password, user_login_data.password_hash)):
            logger.warning(
                "Attempt to login in to user %s with invalid credentials",
                user.login_data.username
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        return LoginResponse(
            access_token=cls.generate_access_token(user.id),
            refresh_token=cls.generate_refresh_token(user.id)
        )

    @classmethod
    def authenticate(cls, credentials: HTTPAuthorizationCredentials = Depends(http_bearer_scheme)):
        """
        Used in controller methods that require authentication.
        """
        user = cls._validate_token(credentials.credentials, "access")

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        return user
