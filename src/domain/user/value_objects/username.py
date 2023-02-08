from src.domain.base.value_objects.base import ValueObject


class Username(ValueObject[str]):
    value: str
