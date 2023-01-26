from dataclasses import dataclass

from src.application.common.exceptions import ApplicationException
from src.domain.user.value_objects import UserId, Username


@dataclass(eq=False)
class UserIdAlreadyExist(ApplicationException):
    user_id: UserId


@dataclass(eq=False)
class UsernameAlreadyExist(ApplicationException):
    username: Username


@dataclass(eq=False)
class UserIdNotExist(ApplicationException):
    user_id: UserId


@dataclass(eq=False)
class UsernameNotExist(ApplicationException):
    username: Username
