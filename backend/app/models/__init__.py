"""
Initialization of database
"""
import logging
from .base import db
from .role import Role
from .user_login_data import UserLoginData
from .user_profile import UserProfile
from .user_role import UserRole
from .user_termination import UserTermination
from .user import User

logger = logging.getLogger(__name__)

def create_database():
    """
    Automatically connects to the database and initializes all tables.
    """
    logger.debug("Connecting to databse...")
    db.connect()

    logger.debug("Initializing tables...")
    db.create_tables(
        [
            Role,
            UserLoginData,
            UserProfile,
            UserRole,
            UserTermination,
            User
        ],
        safe=True
    )
