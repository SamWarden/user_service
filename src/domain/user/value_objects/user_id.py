from dataclasses import dataclass
from uuid import UUID

from src.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserId(ValueObject[UUID]):
    value: UUID

    def to_uuid(self) -> UUID:
        return self.value
