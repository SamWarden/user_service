from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class Mapper(Protocol):
    def load(self, data: Any, class_: type[T]) -> T:
        raise NotImplementedError
