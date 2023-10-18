from datetime import datetime, timezone
from typing import Self

from src.domain.common.value_objects import ValueObject


class DeletionTime(ValueObject[datetime | None]):
    value: datetime | None

    @classmethod
    def create_deleted(cls) -> Self:
        return cls(datetime.now(timezone.utc))

    @classmethod
    def create_not_deleted(cls) -> Self:
        return cls(None)

    def is_deleted(self) -> bool:
        return self.value is not None
