from uuid import UUID

from src.domain.base.value_objects.base import ValueObject


class UserId(ValueObject[UUID]):
    def to_uuid(self) -> UUID:
        return self.value
