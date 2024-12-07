"""
Service for managing users.
"""
import logging
import uuid
import random
import peewee as pw
import pendulum as pnd
from fastapi import HTTPException, status

from backend.app.utils.security.hashing import (
    hash_password
)

from backend.app.models.user_login_data import UserLoginData
from backend.app.models.user_profile import UserProfile
from backend.app.models.user_role import UserRole
from backend.app.models.user import User
from backend.app.models.role import Role

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
from backend.app.dtos.user_service.dtos import UserProfile as UserProfileDto

from backend.app.services.auth import AuthService

logger = logging.getLogger(__name__)

class UserService:
    """
    Service for managing users.
    """
    @classmethod
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

            logger.warning(
                "Attempted to register user with existing "
                "username or email (%s, %s)", 
                request.email, request.username
            )

            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Provided username or email is already in use."
        )

        logger.debug("Creating user account for user %s...", request.email)

        user = User(
            registration_date=pnd.now()
            ).save()

        logger.debug("Creating user role for user %s...", request.email)

        UserRole(user=user, role=Role.get_by_name("user")).save()

        logger.debug("Creating user login data for user %s...", request.email)

        UserLoginData(
            user=user,
            username=request.username,
            email=request.email,
            password_hash=hash_password(request.password),
            auth_token_salt=str(uuid.uuid4()),
            is_email_confirmed=False,
            confirmation_code=str(random.randint(100000, 999999)),
            confirmation_gen_time=pnd.now(),
            recovery_token=str(uuid.uuid4()),
            recovery_gen_time=pnd.now()
        ).save()

        logger.debug(
            "Registration code for user %s is %s",
            request.email, user.login_data.confirmation_code
        )

        return BeginRegistrationResponse(
            success=True
        )

    @classmethod
    def check_registration_code(
        cls, request: CheckRegistrationCodeRequest) -> CheckRegistrationCodeResponse:
        """
        Check registration code. Regenerates code if expired.
        """
        logger.debug("Checking registration code for user %s...", request.email)
        user: User
        try:
            user = User.get_by_email(request.email)

            if ((not user.login_data.is_email_confirmed) and
            pnd.instance(user.login_data.confirmation_gen_time).add(minutes=10) < pnd.now()):

                logger.debug("Code expired for user %s, regenerating...", request.email)

                # Regenerate code
                code = str(random.randint(100000, 999999))
                login_data = UserLoginData.get(user=user)
                login_data.confirmation_code = code
                login_data.confirmation_gen_time = pnd.now()
                login_data.save()

                logger.debug("New registration code for user %s is %s", request.email, code)

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Code expired"
                )

            # Check if email is already confirmed or code is invalid
            if (user.login_data.is_email_confirmed or
                user.login_data.confirmation_code != request.confirmation_code):
                logger.warning("Invalidated confirmation code for user %s", request.email)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid account or confirmation code"
                )
            return CheckRegistrationCodeResponse(success=True)

        except pw.DataError as e:
            logger.error("Failed to obtain user %s: %s", request.email, e)
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid account or confirmation code"
                ) from e

    @classmethod
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

        logger.debug("Marking user %s as confirmed...", request.email)

        user = User.get_by_email(request.email)

        # Set email as confirmed
        login_data = UserLoginData.get(user=user)
        login_data.is_email_confirmed = True
        login_data.save()

        logger.debug("Creating user profile for user %s (%s)...", request.email, user.id)

        # Create user profile
        UserProfile(
            user=user,
            name=request.name,
            surname=request.surname,
            patronymic=request.patronymic,
            avatar_url=request.avatar_url
        ).save()

        logger.debug("Issuing tokens for user %s...", user.id)

        # Finish registration and return access and refresh tokens
        return CompleteRegistrationResponse(
            access_token=AuthService.generate_access_token(user.id),
            refresh_token=AuthService.generate_refresh_token(user.id)
        )

    @classmethod
    def get_user_profile(cls, user_id) -> UserProfileDto:
        """
        Get user profile.
        """
        profile = User.get_by_id(user_id).profile
        return UserProfileDto(
            name=profile.name,
            surname=profile.surname,
            patronymic=profile.patronymic,
            avatar_url=profile.avatar_url
        )
