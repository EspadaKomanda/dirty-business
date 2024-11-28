"""
Testing database operations, including database initialization, entity creation
and entity validation.
"""
import unittest
from app import config

config.ENVIRONMENT_TYPE = "development"
config.POSTGRES_DB = "automatic_unittest_database"

class TestDatabase(unittest.TestCase):
    """
    Testing database operations, including database initialization, entity creation
    and entity validation.
    """

    def creation(self):
        """Create the database"""
        return True

    def wiping(self):
        """Wipe the database"""
        return True
