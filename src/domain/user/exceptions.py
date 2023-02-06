from dataclasses import dataclass

from src.domain.base.exceptions import DomainException


@dataclass(eq=False)
class UserIsDeleted(RuntimeError, DomainException):
    user_id: int
