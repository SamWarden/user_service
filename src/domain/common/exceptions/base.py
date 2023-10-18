from dataclasses import dataclass
from typing import ClassVar


@dataclass(eq=False)
class AppException(Exception):
    """Base Exception"""

    status: ClassVar[int] = 500

    @property
    def title(self) -> str:
        return "An app error occurred"


class DomainException(AppException):
    """Base Domain Exception"""

    @property
    def title(self) -> str:
        return "A domain error occurred"
