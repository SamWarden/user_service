from src.application.user import dto
from src.domain.base.constants import Empty
from src.presentation.api.controllers import responses


def convert_dto_to_users_response(users: dto.Users) -> responses.Users:
    users_response = responses.Users(
        users=users.users,
        total=users.total,
        offset=users.offset if users.offset is not Empty.UNSET else None,
        limit=users.limit if users.limit is not Empty.UNSET else None,
    )

    return users_response
