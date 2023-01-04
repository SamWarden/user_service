import time
from typing import Self

from src.domain.base.exceptions import DomainException

from .base import ValueObject


class NegativeTimestamp(DomainException, ValueError):
    pass


class Timestamp(ValueObject[int]):
    def _validate(self) -> None:
        if self.value < 0:
            raise NegativeTimestamp

    @classmethod
    def now(cls) -> Self:
        return cls(int(time.time() * 1000))
