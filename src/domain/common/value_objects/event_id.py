from typing import Self
from uuid import UUID

from uuid6 import uuid7

from src.domain.common.value_objects.base import ValueObject


class EventId(ValueObject[UUID]):
    value: UUID

    @classmethod
    def generate(cls) -> Self:
        return cls(uuid7())
