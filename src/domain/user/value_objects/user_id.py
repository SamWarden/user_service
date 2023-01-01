from uuid import UUID

from src.domain.base.value_objects.base import ValueObject


class UserId(ValueObject[UUID]):
    pass
