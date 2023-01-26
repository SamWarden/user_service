from .deleted_user import DeletedUser
from .user import User

UserDTOs = User | DeletedUser

__all__ = (
    "DeletedUser",
    "User",
    "UserDTOs",
)
