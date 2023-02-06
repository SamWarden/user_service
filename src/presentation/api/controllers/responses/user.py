from dataclasses import dataclass

from src.application.user import dto


@dataclass(frozen=True)
class Users:
    users: tuple[dto.UserDTOs, ...]
