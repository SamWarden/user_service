from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class DeletedUser(DTO):
    id: UUID
    first_name: str
    last_name: str
    middle_name: str | None
    deleted_at: datetime
    username: None = field(init=False, default=None)

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
