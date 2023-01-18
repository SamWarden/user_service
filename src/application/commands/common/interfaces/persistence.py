from typing import Protocol

from src.domain.user.entities import User
from src.domain.user.value_objects import UserId


class UserRepo(Protocol):
    async def get_user_by_id(self, user_id: UserId) -> User:
        raise NotImplementedError
