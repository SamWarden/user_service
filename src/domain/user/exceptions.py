from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions import DomainException


@dataclass(eq=False)
class UserIsDeleted(RuntimeError, DomainException):
    user_id: UUID

    @property
    def message(self) -> str:
        return f'The user with "{self.user_id}" user_id is deleted'
