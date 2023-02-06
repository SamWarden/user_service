from src.domain.base.exceptions import DomainException


class UserIsDeleted(RuntimeError, DomainException):
    user_id: int
