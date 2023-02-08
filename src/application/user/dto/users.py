from dataclasses import dataclass

from src.domain.base.constants import Empty
from .deleted_user import DeletedUser
from .user import User

UserDTOs = User | DeletedUser


@dataclass(frozen=True)
class Users:
    users: tuple[UserDTOs, ...]
    total: int
    offset: int | Empty = Empty.UNSET
    limit: int | Empty = Empty.UNSET
