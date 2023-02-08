import re
from dataclasses import dataclass

from src.application.common.exceptions import ApplicationException

MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


@dataclass(eq=False)
class WrongUsernameValue(ValueError, ApplicationException):
    username: str


class TooLongUsername(WrongUsernameValue):
    pass


class EmptyUsername(WrongUsernameValue):
    pass


class WrongUsernameFormat(WrongUsernameValue):
    pass


def validate_username(username: str) -> None:
    if username == "":
        raise EmptyUsername(username)
    if not USERNAME_PATTERN.match(username):
        raise WrongUsernameFormat(username)
    if len(username) > MAX_USERNAME_LENGTH:
        raise TooLongUsername(username)
