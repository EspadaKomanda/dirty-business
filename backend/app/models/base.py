"""
Base model for peewee database
"""
import json
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

    class Meta:
        """
        Metadata for the database model
        """
        database = db

    def to_dict(self):
        """Converts the object to a dictionary"""
        return self.__dict__

    def to_json(self):
        """Converts the object to a JSON string"""
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()

    def validate(self):
        """
        Function to run validation on.
        """
        return self

    def save(self, *args, **kwargs):
        self.validate()

        # Update the updated_at field before saving
        self.updated_at = pnd.now()

        super().save(*args, **kwargs)
        return self
