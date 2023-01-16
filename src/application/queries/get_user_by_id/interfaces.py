from typing import Protocol

from src.application.common.user import dto
from src.application.queries.common.interfaces.persistence import UserReader as _UserReader
from src.domain.user.value_objects import UserId


class UserReader(_UserReader, Protocol):
    async def get_user_by_id(self, user_id: UserId) -> dto.User:
        raise NotImplementedError
