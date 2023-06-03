import re
from dataclasses import dataclass

from src.domain.common.exceptions import DomainException
from src.domain.common.value_objects.base import ValueObject

MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


@dataclass(eq=False)
class WrongUsernameValue(ValueError, DomainException):
    username: str


class EmptyUsername(WrongUsernameValue):
    @property
    def message(self) -> str:
        return "Username can't be empty"


class TooLongUsername(WrongUsernameValue):
    @property
    def message(self) -> str:
        return f'Too long username "{self.username}"'


class WrongUsernameFormat(WrongUsernameValue):
    @property
    def message(self) -> str:
        return f'Wrong username format "{self.username}"'


@dataclass(frozen=True)
class Username(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) == 0:
            raise EmptyUsername(self.value)
        if len(self.value) > MAX_USERNAME_LENGTH:
            raise TooLongUsername(self.value)
        if not USERNAME_PATTERN.match(self.value):
            raise WrongUsernameFormat(self.value)
