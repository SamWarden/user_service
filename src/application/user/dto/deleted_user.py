from dataclasses import dataclass, field
from typing import Literal
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class DeletedUser(DTO):
    id: UUID
    first_name: str
    last_name: str | None
    deleted: Literal[True] = field(default=True, init=False)

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
