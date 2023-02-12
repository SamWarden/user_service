from src.domain.common.exceptions import AppException


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


class MappingError(ApplicationException):
    pass
