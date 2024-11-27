"""
Initialization of database
"""
import logging
from .base import db

logger = logging.getLogger(__name__)

def create_database():
    """
    Automatically connects to the database and initializes all tables.
    """
    logger.debug("Connecting to databse...")
    db.connect()
    
    logger.debug("Initializing tables...")
    db.create_tables([], safe=True)
