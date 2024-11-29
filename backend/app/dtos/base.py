"""
Base class for a data transfer object
"""
import json
from dataclasses import dataclass
from backend.app.utils.sanitization.standard import sanitize_all

@dataclass
class BaseDto():
    """
    Base class for a data transfer object. Automatically applies validation
    """
    def to_dict(self):
        """Converts the object to a dictionary"""
        return self.__dict__

    def to_json(self):
        """Converts the object to a JSON string"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str):
        """Converts a JSON string to Dto object"""
        return cls(**json.loads(json_str))

    @classmethod
    def from_dict(cls, dict_obj: dict):
        """Converts a dictionary to Dto object"""
        return cls(**dict_obj)

    def __str__(self):
        return self.to_json()

    @sanitize_all()
    def sanitize(self):
        """
        Used for field sanitization. When necessary to exclude fields,
        apply @sanitize_all(exclude=["field1", "field2"]) on method manually.
        """
        return self

    def clean(self):
        """
        Used for class validation. Triggered after sanitization.
        Does not perform any actions by default.
        """
        return self

    def validate(self):
        """
        Performs sanitization and validation.
        Returns the result object.
        """
        return self.sanitize().clean()

    def __post_init__(self):
        """Run validation after initialization"""
        self.validate()
