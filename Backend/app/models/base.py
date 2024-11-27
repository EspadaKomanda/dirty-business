"""
Base model for peewee database
"""
import pendulum as pnd
import peewee as pw
from config import POSTGRES_HOSTNAME, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

db = pw.PostgresqlDatabase(
    POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOSTNAME,
    port=POSTGRES_PORT
)

class BaseModel(pw.Model):
    """
    Default database model
    """
    created_at = pw.DateTimeField(default=pnd.now())
    updated_at = pw.DateTimeField(default=pnd.now())

    class Meta:
        """
        Metadata for the database model
        """
        database = db  # This model uses the PostgreSQL database

    def save(self, *args, **kwargs):
        # Update the updated_at field before saving
        self.updated_at = pnd.now()
        return super().save(*args, **kwargs)