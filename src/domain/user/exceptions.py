from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions import DomainError


@dataclass(eq=False)
class UserIsDeletedError(RuntimeError, DomainError):
    user_id: UUID

    @property
    def title(self) -> str:
        return f'The user with "{self.user_id}" user_id is deleted'


@dataclass(eq=False)
class UsernameAlreadyExistsError(DomainError):
    username: str | None = None

    @property
    def title(self) -> str:
        if self.username is None:
            return "A user with the username already exists"
        return f'A user with the "{self.username}" username already exists'
