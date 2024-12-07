"""
Service for working with Redis.
"""
import redis
from backend.app.config import (
    REDIS_HOSTNAME,
    REDIS_PORT,
    REDIS_PASSWORD
)

client = redis.Redis(
    host=REDIS_HOSTNAME,
    port=int(REDIS_PORT),
    password=REDIS_PASSWORD,
    db=0
)

class RedisService:
    """
    Service for working with Redis.
    """
    @classmethod
    def set(cls, key: str, value: str):
        """
        Sets a key-value pair in Redis.
        """
        client.set(key, value)

    @classmethod
    def get(cls, key: str):
        """
        Gets a key-value pair from Redis.
        """
        return client.get(key).decode("utf-8")

    @classmethod
    def exists(cls, key: str):
        """
        Checks if a key exists in Redis.
        """
        return client.exists(key)
