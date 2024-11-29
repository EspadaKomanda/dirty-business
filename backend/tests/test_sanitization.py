"""
Tests for validation decorators.
"""
import unittest
from dataclasses import dataclass
import logging
from backend.app.utils.sanitization.standard import (
    sanitize_trim,
    sanitize_all,
    sanitize_capitalize
)

logger = logging.getLogger(__name__)

class TestSanitization(unittest.TestCase):
    """
    Validation tests
    """
    @dataclass
    class TestDTO:
        """Testing class"""

        def clean(self):
            """Class validation"""
            return self

        def __post_init__(self):
            self.clean()

    @classmethod
    def test_standard_sanitization(cls):
        """
        Testing standard sanitization decorators
        """
        @dataclass
        class RegisterRequest(cls.TestDTO):
            """For sanitization testing"""
            name: str

            @sanitize_trim("name")
            @sanitize_capitalize("name")
            def clean(self):
                return self

        for value in [
            "Gustavo Fring",
            "gustavo fring",
            "GUsTavo FrInG",
            "   Gustavo Fring   ",
            "GUSTAVO FRING",
            "  GUSTAVO frIng  "
        ]:
            dto = RegisterRequest(name=value)
            assert dto.name == "Gustavo Fring"

    @classmethod
    def test_sanitize_all(cls):
        """Sanitize trim all test"""

        @dataclass
        class TeamDTO(cls.TestDTO):
            """For sanitization testing"""
            frontend: str = " Rudolf Shevchenko   "
            backend: str = "  Nikolai Papin  "
            capitan: str = "Maxim Doroshko"
            project: str = " "

            @sanitize_all(exclude=["project"])
            def clean(self):
                return self

        dto = TeamDTO()
        assert dto.frontend == "Rudolf Shevchenko"
        assert dto.backend == "Nikolai Papin"
        assert dto.capitan == "Maxim Doroshko"
        assert dto.project == " "
