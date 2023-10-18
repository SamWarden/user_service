from dataclasses import dataclass
from uuid import UUID

from src.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserId(ValueObject[UUID]):
    value: UUID
