from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from user_service.application.common.dto import DTO
from user_service.application.common.pagination.dto import PaginatedItemsDTO


@dataclass(frozen=True)
class User(DTO):
    id: UUID
    username: str | None
    first_name: str
    last_name: str
    middle_name: str | None
    deleted_at: None | datetime

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


Users: TypeAlias = PaginatedItemsDTO[User]
