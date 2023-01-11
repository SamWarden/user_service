from typing import Any, Protocol, Type, TypeVar

T = TypeVar("T")


class Mapper(Protocol):
    def load(self, data: Any, class_: Type[T]) -> T:
        raise NotImplementedError
