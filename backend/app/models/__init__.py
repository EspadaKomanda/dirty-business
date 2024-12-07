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
from .camera import Camera

logger = logging.getLogger(__name__)

tables = [
        Role,
        UserLoginData,
        UserProfile,
        UserRole,
        UserTermination,
        User,
        Camera
    ]

logger.debug("Connecting to databse...")
db.connect()

def create_database():
    """
    Automatically initializes all tables.
    """
    logger.debug("Initializing tables...")
    db.create_tables(
        tables,
        safe=True
    )

    Role(name="user")
    Role(name="admin")

    if Camera.select().count() != 0:  # pylint: disable=no-value-for-parameter
        return

    Camera(
        id=1,
        name="Dummy 1",
        description="Located in room 12",
        contamination=0.5,
        date="2024-01-01",
        url="https://t4.ftcdn.net/jpg/03/10/07/45/360_F_310074598_rBt50O0nwjydPjWStjdzyNdm0Oh1nAyV.jpg"
    ).save()

    Camera(
        id=2,
        name="Dummy 2",
        description="Located in room 15",
        contamination=0.3,
        date="2024-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    Camera(
        id=3,
        name="Dummy 3",
        description="Located in room 17",
        contamination=0.13,
        date="2022-01-01",
        url="https://media.istockphoto.com/id/1141324902/photo/real-lens-flare-shot-in-studio-over-black-background-easy-to-add-as-overlay-or-screen-filter.jpg?s=612x612&w=0&k=20&c=zWGnDHkDJZKqaUdNIGkf_eSNJ17qRrnl7czqJxWZlLw="
    ).save()

    Camera(
        id=4,
        name="Dummy 4",
        description="Located in room 19",
        contamination=0.1,
        date="2022-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    Camera(
        id=5,
        name="Dummy 5",
        description="Located in room 21",
        contamination=0.05,
        date="2022-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    Camera(
        id=6,
        name="Dummy 6",
        description="Located in room 23",
        contamination=0.01,
        date="2022-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    Camera(
        id=7,
        name="Dummy 7",
        description="Located in room 25",
        contamination=0,
        date="2022-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    Camera(
        id=8,
        name="Dummy 8",
        description="Located in room 27",
        contamination=0,
        date="2022-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    Camera(
        id=9,
        name="Dummy 9",
        description="Located in room 29",
        contamination=0,
        date="2022-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    Camera(
        id=10,
        name="Dummy 10",
        description="Located in room 31",
        contamination=0,
        date="2022-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    Camera(
        id=11,
        name="Dummy 11",
        description="Located in room 33",
        contamination=0,
        date="2022-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    Camera(
        id=12,
        name="Dummy 12",
        description="Located in room 35",
        contamination=0,
        date="2022-01-01",
        url="https://t4.ftcdn.net/jpg/05/00/56/83/360_F_500568328_HdltBEmUOLBcRfIQTzjSslOsfuH06OCh.jpg"
    ).save()

    logger.debug("All tables have been initialized successfully.")

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
