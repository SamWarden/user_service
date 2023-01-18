from typing import Protocol

from src.application.commands.common.interfaces.persistence import UserRepo as _UserRepo
from src.domain.user.entities import User


class UserRepo(_UserRepo, Protocol):
    async def update_user(self, user: User) -> None:
        raise NotImplementedError
