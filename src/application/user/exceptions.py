from dataclasses import dataclass
from uuid import UUID

from src.application.common.exceptions import ApplicationException


@dataclass(eq=False)
class UserIdAlreadyExists(ApplicationException):
    user_id: UUID

    @property
    def title(self) -> str:
        return f'A user with the "{self.user_id}" user_id already exists'


@dataclass(eq=False)
class UserIdNotExist(ApplicationException):
    user_id: UUID

    @property
    def title(self) -> str:
        return f'A user with "{self.user_id}" user_id doesn\'t exist'


@dataclass(eq=False)
class UsernameNotExist(ApplicationException):
    username: str

    @property
    def title(self) -> str:
        return f'A user with "{self.username}" username doesn\'t exist'
