from typing import Self
from uuid import UUID

from uuid_extensions import uuid7

from src.domain.base.value_objects.base import ValueObject


class EventId(ValueObject[UUID]):
    @classmethod
    def generate(cls) -> Self:
        return cls(uuid7())
