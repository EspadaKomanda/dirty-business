"""
Test Dto functionality.
"""
from dataclasses import dataclass
import logging
import unittest
from backend.app.dtos.base import BaseDto
from backend.app.utils.sanitization.standard import sanitize_all
from backend.app.utils.validation.standard import validate_length
from backend.app.exceptions.generic.validation_exception import ValidationException

logger = logging.getLogger(__name__)

class TestDtos(unittest.TestCase):
    """Test Dtos"""

    @dataclass
    class PersonDto(BaseDto):
        """For testing"""
        name: str
        surname: str = None

        @validate_length("name", min_length=1, max_length=5, required=True)
        @validate_length("surname", min_length=1, max_length=5, required=False)
        @sanitize_all()
        def clean(self):
            return self

    @classmethod
    def test_base_dto(cls):
        """Test Base Dto"""

        logger.debug("Testing validation of dto on creation...")
        try:
            cls.PersonDto(name="")
            assert False
        except ValidationException:
            assert True

        try:
            cls.PersonDto(name="John Doe")
            assert False
        except ValidationException:
            assert True

        try:
            cls.PersonDto(name="John    ")
            assert True
        except ValidationException as e:
            logger.error(e)
            assert False

    def test_base_dto_serialization(self):
        """Test Base Dto JSON"""
        logger.debug("Testing serialization and deserialization of dto...")

        dto = self.PersonDto(name="John", surname="Doe")

        json_str = dto.to_json()
        assert json_str == '{"name": "John", "surname": "Doe"}'

        dto = self.PersonDto.from_json(json_str)
        assert dto.surname == "Doe"

        assert (str(dto)) == '{"name": "John", "surname": "Doe"}'

    def test_base_dto_dict_conversion(self):
        """Test Base Dto dict conversion"""
        dto = self.PersonDto(name="John", surname="Doe")
        assert dto.to_dict() == {"name": "John", "surname": "Doe"}

        dto = self.PersonDto.from_dict({"name": "John", "surname": "Doe"})
        assert dto.surname == "Doe"
