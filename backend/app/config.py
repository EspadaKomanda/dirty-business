"""
Configuration file for the application.

Utilizes environment variables and makes them accessible
everywhere else.

Do not modify this file, configure variables in your
environment instead.
"""
import logging
from os import getenv
from dotenv import load_dotenv
from exceptions.generic.configuration_exception import ConfigurationException

load_dotenv(override=False)

# Environment
ENVIRONMENT_TYPE=getenv("ENVIRONMENT_TYPE") or "development"

# PosgreSQL
POSTGRES_HOSTNAME=getenv("POSTGRES_HOSTNAME")
POSTGRES_PORT=getenv("POSTGRES_PORT")
POSTGRES_DB=getenv("POSTGRES_DB")
POSTGRES_USER=getenv("POSTGRES_USER")
POSTGRES_PASSWORD=getenv("POSTGRES_PASSWORD")

if (POSTGRES_HOSTNAME is None or
    POSTGRES_PORT is None or
    POSTGRES_DB is None or
    POSTGRES_USER is None or
    POSTGRES_PASSWORD is None):
    raise ConfigurationException("Not all database parameters have been configured.")

# Redis
REDIS_HOSTNAME=getenv("REDIS_HOSTNAME")
REDIS_PORT=getenv("REDIS_PORT")
REDIS_PASSWORD=getenv("REDIS_PASSWORD")

if REDIS_PASSWORD is None:
    raise ConfigurationException("Redis password have not been configured.")

# Jwt
JWT_KEY=getenv("JWT_KEY")
JWT_ACCESS_EXPIRE_MINUTES=getenv("JWT_ACCESS_EXPIRE_MINUTES")
JWT_REFRESH_EXPIRE_MINUTES=getenv("JWT_REFRESH_EXPIRE_MINUTES")
JWT_ISSUER=getenv("BOT_JWT_ISSUERTOKEN")
JWT_AUDIENCE=getenv("JWT_AUDIENCE")

if (JWT_KEY is None or
    JWT_ACCESS_EXPIRE_MINUTES is None or
    JWT_REFRESH_EXPIRE_MINUTES is None or
    JWT_ISSUER is None or
    JWT_AUDIENCE is None
    ):
    raise ConfigurationException("Not all JWT parameters have been configured.")

# Logging setup
logging.basicConfig(
    level=logging.DEBUG if ENVIRONMENT_TYPE == "development" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)
