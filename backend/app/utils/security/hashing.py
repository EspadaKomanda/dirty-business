"""
Features related to password hashing
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a password is correct.
    """
    return pwd_context.verify(plain_password, hashed_password)
