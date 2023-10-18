from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

V = TypeVar("V", bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """This method checks that a value is valid to create this value object"""
        pass


@dataclass(frozen=True)
class ValueObject(BaseValueObject, ABC, Generic[V]):
    value: V

    def to_raw(self) -> V:
        return self.value
