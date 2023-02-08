from dataclasses import dataclass
from typing import Sequence

from src.application.user import dto


@dataclass(frozen=True)
class Users:
    users: Sequence[dto.UserDTOs]
    total: int
    offset: int | None = None
    limit: int | None = None
