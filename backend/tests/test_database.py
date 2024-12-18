"""
Testing database operations, including database initialization, entity creation
and entity validation.
"""
import unittest
import uuid
import logging
import pendulum as pnd
from backend.app import config, models
from backend.app.models.role import Role
from backend.app.models.user_login_data import UserLoginData
from backend.app.models.user_profile import UserProfile
from backend.app.models.user_role import UserRole
from backend.app.models.user_termination import UserTermination
from backend.app.models.user import User

config.ENVIRONMENT_TYPE = "development"
config.POSTGRES_DB = "automatic_unittest_database"

logger = logging.getLogger(__name__)

class TestDatabase(unittest.TestCase):
    """
    Testing database operations, including database initialization, entity creation
    and entity validation.
    """
    def test_wipe_and_creation(self):
        """Create the database"""
        logger.debug("Initial safe wipe of the database...")
        models.wipe_database("automatic_unittest_database")

        logger.debug("Creation of the database...")
        models.create_database()

        logger.debug("Repeat creation of the database...")
        models.create_database()

        logger.debug("Wipe database again...")
        models.wipe_database("automatic_unittest_database")

    def test_peewee_models(self):
        """Screw around with the tables."""
        logger.debug("Creation of the database...")
        models.create_database()

        logger.debug("Creation of tables...")
        role = Role.create(
            name="princess"
        ).save()

        user = User.create(
            registration_date=pnd.now()
        ).save()

        UserLoginData.create(
            user=user,
            username="username",
            email="email@email.com",
            password_hash="password_hash",
            auth_token_salt=str(uuid.uuid4()),
            is_email_confirmed=True,
            confirmation_code="111111",
            confirmation_gen_time=pnd.now(),
            recovery_token=str(uuid.uuid4()),
            recovery_gen_time=pnd.now()
        ).save()

        UserProfile.create(
            user=user,
            name="name",
            surname="surname",
            patronymic="patronymic",
            avatar_url="http://example.com/images/avatar.png"
        ).save()

        UserRole.create(
            user=user,
            role=role
        ).save()

        UserTermination.create(
            user=user,
            termination_reason="termination_reason",
            termination_gen_time=pnd.now()
        ).save()

        logger.debug("Deleting tables recursively...")
        user.delete_instance(recursive=True)
        role.delete_instance(recursive=True)

    def test_database_validation(self):
        """Validation attributes test"""
        logger.debug("Creation of the database...")
        models.create_database()

        logger.debug("Creation of tables...")

        user = User.create(
            registration_date=pnd.now()
        ).save()

        # Test name validation
        try:
            UserProfile.create(
                user=user,
                name="name",
                surname="surname",
                patronymic="pat"*100,
                avatar_url="example.com/images/avatar.png"
            ).save()
            assert False
        except ValueError:
            pass

        # Test email validation
        try:
            UserLoginData.create(
                user=user,
                username="username",
                email="email",
                password_hash="password_hash",
                auth_token_salt="auth_token_salt",
                is_email_confirmed=True,
                confirmation_code="111111",
                confirmation_gen_time=pnd.now(),
                recovery_token="recovery_token",
                recovery_gen_time=pnd.now()
            ).save()
            assert False
        except ValueError:
            pass

        logger.debug("Deleting tables recursively...")
        user.delete_instance(recursive=True)
