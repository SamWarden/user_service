from dataclasses import dataclass
from uuid import UUID

from user_service.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class UserId(ValueObject[UUID]):
    value: UUID
