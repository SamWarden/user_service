import re

from src.domain.base.exceptions import DomainException
from src.domain.base.value_objects.base import ValueObject

MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


class WrongUsernameValue(ValueError, DomainException):
    pass


class TooLongUsername(WrongUsernameValue):
    pass


class EmptyUsername(WrongUsernameValue):
    pass


class WrongUsernameFormat(WrongUsernameValue):
    pass


class Username(ValueObject[str]):
    def _validate(self) -> None:
        if self.value == "":
            raise EmptyUsername
        if not USERNAME_PATTERN.match(self.value):
            raise WrongUsernameFormat
        if len(self.value) > MAX_USERNAME_LENGTH:
            raise TooLongUsername
