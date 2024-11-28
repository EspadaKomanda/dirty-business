"""
Testing database operations, including database initialization, entity creation
and entity validation.
"""
import unittest
from backend.app import config, models

config.ENVIRONMENT_TYPE = "development"
config.POSTGRES_DB = "automatic_unittest_database"

class TestDatabase(unittest.TestCase):
    """
    Testing database operations, including database initialization, entity creation
    and entity validation.
    """

    def test_creation(self):
        """Create the database"""
        models.create_database()


    def test_wiping(self):
        """Wipe the database"""
        models.wipe_database("automatic_unittest_database")
