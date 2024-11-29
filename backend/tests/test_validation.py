"""
Tests for validation decorators.
"""
import unittest
from dataclasses import dataclass
import logging
from backend.app.utils.validation.standard import (
    validate_url,
    validate_length
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
    def test_url_regex_handler(cls):
        """
        Testing standard regex validation decorator
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

    @classmethod
    def test_validate_length(cls):
        """
        Testing standard length validation decorator
        """
        @dataclass
        class LengthTestDTO(cls.TestDTO):
            """For testing length decorators"""

            phone: str = "11111111111"
            username: str = "username"
            password: str = "verysecuredamnpassword"
            bio: str = "Talanted gamer"

            @validate_length("phone", precise_length=11)
            @validate_length("username", 3, 10)
            @validate_length("password", 8)
            @validate_length("bio", max_length=75)
            def clean(self):
                return self

        logger.debug("Testing on valid lengths...")

        try:
            LengthTestDTO()
        except ValidationException:
            logger.error("Valid length did not pass")
            assert False

        logger.debug("Testing on invalid lengths...")

        for value in ["", "123456", "12345678901234567890"]:
            try:
                LengthTestDTO(phone=value)
                logger.error("Invalid length passed")
                assert False
            except ValidationException:
                continue

        for value in ["a", "aa", "Xx_EngineerGaming_xX"]:
            try:
                LengthTestDTO(username=value)
                logger.error("Invalid username length passed")
                assert False
            except ValidationException:
                continue

        for value in ["dog", "gooddog", "superve"]:
            try:
                LengthTestDTO(password=value)
                logger.error("Invalid password length passed")
                assert False
            except ValidationException:
                continue

        try:
            LengthTestDTO(bio="a"*76)
            logger.error("Invalid bio length passed:")
            assert False
        except ValidationException:
            pass
