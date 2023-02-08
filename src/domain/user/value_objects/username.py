from src.domain.common.value_objects.base import ValueObject


class Username(ValueObject[str]):
    value: str
