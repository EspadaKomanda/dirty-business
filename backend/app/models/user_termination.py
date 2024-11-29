"""
Object representing a user termination.
"""
import peewee as pw
from backend.app.utils.sanitization.standard import sanitize_all
from backend.app.utils.validation.standard import validate_length
from .base import Base
from .user import User

class UserTermination(Base):
    """
    Object representing a user termination.
    """
    user = pw.ForeignKeyField(User, backref="user_termination", unique=True, on_delete="CASCADE")
    reason = pw.CharField(null=True, max_length=1000)
    termination_date = pw.TimestampField()

    @sanitize_all()
    @validate_length("reason", max_length=1000)
    def clean(self):
        """validation"""
        return self
