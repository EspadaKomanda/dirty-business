"""
Initialization of database
"""
import logging
from backend.app.config import POSTGRES_DB, ENVIRONMENT_TYPE
from .base import db
from .role import Role
from .user_login_data import UserLoginData
from .user_profile import UserProfile
from .user_role import UserRole
from .user_termination import UserTermination
from .user import User

logger = logging.getLogger(__name__)

tables = [
        Role,
        UserLoginData,
        UserProfile,
        UserRole,
        UserTermination,
        User
    ]

def create_database():
    """
    Automatically connects to the database and initializes all tables.
    """
    logger.debug("Connecting to databse...")
    db.connect()

    logger.debug("Initializing tables...")
    db.create_tables(
        tables,
        safe=True
    )

def wipe_database(database_name: str):
    """
    Removes the contents of the database being used. the database_name parameter is
    compared to the name of the open database to avoid deletion of the wrong database.
    Running wipe_database in an environment other than "development" is also forbidden.
    """
    logger.debug("Wiping database")

    if POSTGRES_DB != database_name:
        raise RuntimeError(
            f"Attempting to wipe a different database. "
            f"Currently running with {POSTGRES_DB}"
        )
    if ENVIRONMENT_TYPE != "development":
        raise RuntimeError("Attempting to wipe database in non-development environment.")

    db.drop_tables(tables, safe=True)

    logger.debug("All tables have been dropped successfully.")
