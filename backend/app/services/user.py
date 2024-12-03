"""
Service for managing users.
"""
import uuid
import peewee as pw
import pendulum as pnd
from fastapi import HTTPException, status

from backend.app.models.base import db

from backend.app.utils.security.hashing import (
    hash_password
)

from backend.app.models.user_login_data import UserLoginData
from backend.app.models.user_profile import UserProfile
# from backend.app.models.user_role import UserRole
# from backend.app.models.user_termination import UserTermination
from backend.app.models.user import User

from backend.app.dtos.user_service.requests import (
    BeginRegistrationRequest,
    CheckRegistrationCodeRequest,
    CompleteRegistrationRequest,
)
from backend.app.dtos.user_service.responses import (
    BeginRegistrationResponse,
    CheckRegistrationCodeResponse,
    CompleteRegistrationResponse
)

from backend.app.services.auth import AuthService

class UserService:
    """
    Service for managing users.
    """
    @classmethod
    @db.atomic
    def begin_registration(
        cls, request: BeginRegistrationRequest) -> BeginRegistrationResponse:
        """
        Begin user registration.
        """
        # Check if user already exists
        if UserLoginData.select().where(
            UserLoginData.email == request.email or
            UserLoginData.username == request.username
        ).exists():
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Provided username or email is already in use."
        )

        user = User(
            registration_date=pnd.now()
            ).save()

        UserLoginData(
            user=user,
            username=request.username,
            email=request.email,
            password_hash=hash_password(request.password),
            auth_token_salt=str(uuid.uuid4()),
            is_email_confirmed=False,
            confirmation_code=str(uuid.uuid4()),
            confirmation_gen_time=pnd.now(),
            recovery_token=str(uuid.uuid4()),
            recovery_gen_time=pnd.now()
        ).save()

        return BeginRegistrationResponse(
            success=True
        )

    @classmethod
    def check_registration_code(
        cls, request: CheckRegistrationCodeRequest) -> CheckRegistrationCodeResponse:
        """
        Check registration code.
        """
        user: User
        try:
            user = User.get_by_email(request.email)

            # Check if email is already confirmed or code is invalid
            if (user.login_data.is_email_confirmed or
                user.login_data.confirmation_code != request.confirmation_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid account or confirmation code"
                )
            return CheckRegistrationCodeResponse(success=True)

        except pw.DataError as e:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid account or confirmation code"
                ) from e

    @classmethod
    @db.atomic
    def complete_registration(
        cls, request: CompleteRegistrationRequest) -> CompleteRegistrationResponse:
        """
        Complete user registration.
        """
        if not cls.check_registration_code(
            CheckRegistrationCodeRequest(
                email=request.email,
                confirmation_code=request.confirmation_code)
            ).success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid account or confirmation code"
            )

        user = User.get_by_email(request.email)
        user.login_data.is_email_confirmed = True

        # Create user profile
        UserProfile(
            user=user,
            name=request.name,
            surname=request.surname,
            patronymic=request.patronymic,
            avatar_url=request.avatar_url
        ).save()

        # Finish registration and return access and refresh tokens
        return CompleteRegistrationResponse(
            access_token=AuthService.generate_access_token(user.id),
            refresh_token=AuthService.generate_refresh_token(user.id)
        )
