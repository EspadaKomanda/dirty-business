"""
Configuration file for the application.

Utilizes environment variables and makes them accessible
everywhere else.

Do not modify this file, configure variables in your
environment instead.
"""
from os import getenv
from dotenv import load_dotenv
from .exceptions.generic.configuration_exception import ConfigurationException

load_dotenv(override=False)

# Environment
ENVIRONMENT_TYPE=getenv("ENVIRONMENT_TYPE") or "development"

# Minio
MINIO_HOSTNAME=getenv("MINIO_HOSTNAME") or "minio"
MINIO_PORT=getenv("MINIO_PORT") or "9000"
MINIO_ROOT_USER=getenv("MINIO_ROOT_USER") or "minio"
MINIO_ROOT_PASSWORD=getenv("MINIO_ROOT_PASSWORD") or "minio"

if (MINIO_HOSTNAME is None or
    MINIO_PORT is None or
    MINIO_ROOT_USER is None or
    MINIO_ROOT_PASSWORD is None):
    raise ConfigurationException("Not all minio parameters have been configured.")

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

if (REDIS_HOSTNAME is None or
    REDIS_PORT is None or
    REDIS_PASSWORD is None):
    raise ConfigurationException("Redis password have not been configured.")

# Jwt
JWT_KEY=getenv("JWT_KEY")
JWT_ACCESS_EXPIRE_MINUTES=getenv("JWT_ACCESS_EXPIRE_MINUTES")
JWT_REFRESH_EXPIRE_MINUTES=getenv("JWT_REFRESH_EXPIRE_MINUTES")
JWT_ISSUER=getenv("JWT_ISSUER")
JWT_AUDIENCE=getenv("JWT_AUDIENCE")
JWT_ALGORITHM=getenv("JWT_ALGORITHM") or "HS256"

if (JWT_KEY is None or
    JWT_ACCESS_EXPIRE_MINUTES is None or
    JWT_REFRESH_EXPIRE_MINUTES is None or
    JWT_ISSUER is None or
    JWT_AUDIENCE is None or
    JWT_ALGORITHM is None
    ):
    raise ConfigurationException("Not all JWT parameters have been configured.")
