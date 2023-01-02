from dataclasses import dataclass

from src.application.base.dto import DTO
from src.domain.user.value_objects import UserId, Username


@dataclass(frozen=True)
class User(DTO):
    id: UserId
    first_name: str
    last_name: str | None
    username: Username

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
