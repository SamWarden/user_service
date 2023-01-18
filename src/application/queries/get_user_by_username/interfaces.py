from typing import Protocol

from src.application.common.user import dto
from src.application.queries.common.interfaces.persistence import UserReader as _UserReader
from src.domain.user.value_objects import Username


class UserReader(_UserReader, Protocol):
    async def get_user_by_username(self, username: Username) -> dto.User:
        raise NotImplementedError
