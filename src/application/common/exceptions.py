from dataclasses import dataclass

from src.domain.common.exceptions import AppException


class ApplicationException(AppException):
    """Base Application Exception"""

    @property
    def title(self) -> str:
        return "An application error occurred"


class UnexpectedError(ApplicationException):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass


class RepoError(UnexpectedError):
    pass


@dataclass(eq=False)
class MappingError(ApplicationException):
    _text: str

    @property
    def title(self) -> str:
        return self._text
