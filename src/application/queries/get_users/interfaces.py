from typing import Protocol

from src.application.common.user import dto
from src.application.queries.common.interfaces.persistence import UserReader as _UserReader


class UserReader(_UserReader, Protocol):
    async def get_users(self) -> tuple[dto.User, ...]:
        raise NotImplementedError
