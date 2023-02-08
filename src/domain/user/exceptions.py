from dataclasses import dataclass
from uuid import UUID

from src.domain.base.exceptions import DomainException


@dataclass(eq=False)
class UserIsDeleted(RuntimeError, DomainException):
    user_id: UUID
