import time
from typing import Self

from .base import ValueObject
from ..exceptions import AppException


class NegativeTimestamp(AppException, ValueError):
    pass


class Timestamp(ValueObject[int]):
    @classmethod
    def validate_value(cls, value: int) -> None:
        if value < 0:
            raise NegativeTimestamp

    @classmethod
    def now(cls) -> Self:
        return cls(int(time.time() * 1000))
