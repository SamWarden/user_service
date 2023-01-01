from abc import ABC
from typing import Any, Generic, TypeVar

V = TypeVar("V", bound=Any)


class ValueObject(Generic[V], ABC):
    value: V

    def __init__(self, value: V) -> None:
        self.validate_value(value)
        self.value = value

    @classmethod
    def validate_value(cls, value: V) -> None:
        """This method checks that a value is valid to create this value object"""
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return self.value
