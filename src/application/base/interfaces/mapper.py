from typing import Any, Protocol, Type, TypeVar

T = TypeVar("T")


class Mapper(Protocol):
    def convert(self, data: Any, class_: Type[T]) -> T:
        raise NotImplementedError
