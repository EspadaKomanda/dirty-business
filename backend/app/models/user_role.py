"""
Object representing the junction table for user and role.
"""
import peewee as pw
from .base import Base
from .user import User
from .role import Role

class UserRole(Base):
    """
    Object representing the junction table for user and role.
    """
    user = pw.ForeignKeyField(User, backref="user_roles", on_delete="CASCADE")
    role = pw.ForeignKeyField(Role, backref="user_roles", on_delete="CASCADE")
