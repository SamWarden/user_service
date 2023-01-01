import re

from src.domain.base.exceptions import AppException
from src.domain.base.value_objects.base import ValueObject

MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


class WrongUsernameValue(ValueError, AppException):
    pass


class TooLongUsername(WrongUsernameValue):
    pass


class EmptyUsername(WrongUsernameValue):
    pass


class WrongUsernameFormat(WrongUsernameValue):
    pass


class Username(ValueObject[str]):
    @classmethod
    def validate_value(cls, value: str) -> None:
        if value == "":
            raise EmptyUsername
        if not USERNAME_PATTERN.match(value):
            raise WrongUsernameFormat
        if len(value) > MAX_USERNAME_LENGTH:
            raise TooLongUsername
