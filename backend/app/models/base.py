"""
Base model for peewee database
"""
import pendulum as pnd
import peewee as pw
from backend.app.config import (
    POSTGRES_HOSTNAME,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)

db = pw.PostgresqlDatabase(
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOSTNAME,
    port=POSTGRES_PORT
)

class Base(pw.Model):
    """
    Default database model
    """
    created_at = pw.DateTimeField(default=pnd.now())
    updated_at = pw.DateTimeField(default=pnd.now())

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Metadata for the database model
        """
        database = db

    def clean(self):
        """validation"""
        return self

    def save(self, *args, **kwargs):
        # Update the updated_at field before saving
        self.clean()
        self.updated_at = pnd.now()
        super().save(*args, **kwargs)
        return self
