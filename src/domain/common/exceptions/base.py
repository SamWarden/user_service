class AppException(Exception):
    """Base Exception"""

    @property
    def message(self) -> str:
        return "An application error occurred"


class DomainException(AppException):
    """Base Domain Exception"""
