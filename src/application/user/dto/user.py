from dataclasses import dataclass, field
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class User(DTO):
    id: UUID
    username: str
    first_name: str
    last_name: str
    middle_name: str | None
    deleted_at: None = field(default=None, init=False)

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
