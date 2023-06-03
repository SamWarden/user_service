import re
from dataclasses import dataclass

from src.domain.common.exceptions import DomainException
from src.domain.common.value_objects.base import BaseValueObject

MAX_NAME_LENGTH = 32
NAME_PATTERN = re.compile(r"[A-Za-z]+")


@dataclass(eq=False)
class WrongNameValue(ValueError, DomainException):
    name: str
    text: str

    @property
    def message(self) -> str:
        return self.text


class EmptyName(WrongNameValue):
    pass


class TooLongName(WrongNameValue):
    pass


class WrongNameFormat(WrongNameValue):
    pass


@dataclass(frozen=True)
class FullName(BaseValueObject):
    first_name: str
    last_name: str
    middle_name: str | None = None

    def _validate(self) -> None:
        if len(self.first_name) == 0:
            raise EmptyName(self.first_name, "First name can't be empty")
        if len(self.first_name) > MAX_NAME_LENGTH:
            raise TooLongName(self.first_name, f'Too long first name "{self.first_name}"')
        if NAME_PATTERN.match(self.first_name) is None:
            raise WrongNameFormat(self.first_name, f'Wrong first name format "{self.first_name}"')

        if len(self.last_name) == 0:
            raise EmptyName(self.last_name, "Last name can't be empty")
        if len(self.last_name) > MAX_NAME_LENGTH:
            raise TooLongName(self.last_name, f'Too long last name "{self.last_name}"')
        if NAME_PATTERN.match(self.last_name) is None:
            raise WrongNameFormat(self.last_name, f'Wrong last name format "{self.last_name}"')

        if self.middle_name is not None:
            if len(self.middle_name) == 0:
                raise EmptyName(self.middle_name, "Middle name can't be empty")
            if len(self.middle_name) > MAX_NAME_LENGTH:
                raise TooLongName(self.middle_name, f'Too long middle name "{self.middle_name}"')
            if NAME_PATTERN.match(self.middle_name) is None:
                raise WrongNameFormat(self.middle_name, f'Wrong middle name format "{self.middle_name}"')

    def __str__(self) -> str:
        if self.middle_name is None:
            return f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.middle_name} {self.last_name}"
