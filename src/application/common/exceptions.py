from src.domain.base.exceptions import AppException


class ApplicationException(AppException):
    pass


class UnexpectedError(ApplicationException):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass


class RepoError(UnexpectedError):
    pass
