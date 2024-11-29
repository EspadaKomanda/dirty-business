"""
Tests for validation decorators.
"""
import unittest
from dataclasses import dataclass
import logging
from backend.app.utils.validation.standard import (
    validate_url
)
from backend.app.exceptions.generic.validation_exception import ValidationException

logger = logging.getLogger(__name__)

class TestValidation(unittest.TestCase):
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
    def test_standard_handlers(cls):
        """
        Testing standard validation decorators
        """
        @dataclass
        class UrlTestDTO(cls.TestDTO):
            """For testing url decorators"""

            url: str = "https://fsf.org"

            @validate_url("url")
            def clean(self):
                return self

        logger.debug("Testing on valid urls...")
        for value in [
            "fsf.org",
            "https://fsf.org",
            "https://fsf.org/",
            "https://shop.fsf.org/",
            "https://good.shop.fsf.org",
            "https://булочки.рф/",
            "https://булочки.рф/buy?a=1&b=2&c=3"
        ]:
            try:
                dto = UrlTestDTO(url=value)
            except ValidationException:
                logger.error("Valid url did not pass: %s", value)
                assert False
            del dto

        logger.debug("Testing on invalid urls...")
        for value in [
            "http:/something.com",
            "https://something.c",
            "https://so..mething.com",
            "https://something..com/",
            "something"]:
            try:
                dto = UrlTestDTO(url=value)
                logger.error("Invalid url passed: %s", value)
                assert False
            except ValidationException:
                continue
