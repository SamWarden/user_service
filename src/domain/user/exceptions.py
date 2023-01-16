from src.domain.base.exceptions import DomainException


class UserAlreadyDeleted(RuntimeError, DomainException):
    pass
