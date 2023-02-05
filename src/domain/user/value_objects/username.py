import re
from dataclasses import dataclass

from src.domain.base.exceptions import DomainException
from src.domain.base.value_objects.base import ValueObject

MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


@dataclass(eq=False)
class WrongUsernameValue(ValueError, DomainException):
    username: str


class TooLongUsername(WrongUsernameValue):
    pass


class EmptyUsername(WrongUsernameValue):
    pass


class WrongUsernameFormat(WrongUsernameValue):
    pass


class Username(ValueObject[str]):
    def _validate(self) -> None:
        if self.value == "":
            raise EmptyUsername(self.value)
        if not USERNAME_PATTERN.match(self.value):
            raise WrongUsernameFormat(self.value)
        if len(self.value) > MAX_USERNAME_LENGTH:
            raise TooLongUsername(self.value)
