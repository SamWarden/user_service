from collections.abc import Callable, Hashable
from typing import Any


class Stub:
    def __init__(self, dependency: Callable, **kwargs: Hashable) -> None:
        self._dependency = dependency
        self._kwargs = kwargs

    def __call__(self):
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Stub):
            return self._dependency == other._dependency and self._kwargs == other._kwargs
        else:
            if not self._kwargs:
                return self._dependency == other
            return False

    def __hash__(self) -> int:
        if not self._kwargs:
            return hash(self._dependency)
        serial = (
            self._dependency,
            *self._kwargs.items(),
        )
        return hash(serial)
