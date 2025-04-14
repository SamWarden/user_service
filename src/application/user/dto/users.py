from typing import TypeAlias

from src.application.common.pagination.dto import PaginatedItemsDTO

from .deleted_user import DeletedUser
from .user import User

UserDTOs: TypeAlias = User | DeletedUser
Users: TypeAlias = PaginatedItemsDTO[UserDTOs]
