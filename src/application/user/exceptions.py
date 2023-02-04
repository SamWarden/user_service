from dataclasses import dataclass
from uuid import UUID

from src.application.common.exceptions import ApplicationException


@dataclass(eq=False)
class UserIdAlreadyExist(ApplicationException):
    user_id: UUID


@dataclass(eq=False)
class UsernameAlreadyExist(ApplicationException):
    username: str


@dataclass(eq=False)
class UserIdNotExist(ApplicationException):
    user_id: UUID


@dataclass(eq=False)
class UsernameNotExist(ApplicationException):
    username: str
