from src.application.user import dto
from src.application.user.commands.update_user import UpdateUserData
from src.domain.common.constants import Empty
from src.presentation.api.controllers import requests, responses


def convert_request_to_update_user_command(request: requests.UpdateUserData) -> UpdateUserData:
    return UpdateUserData(
        username=request.get("username", Empty.UNSET),
        first_name=request.get("first_name", Empty.UNSET),
        last_name=request.get("last_name", Empty.UNSET),
    )


def convert_dto_to_users_response(users: dto.Users) -> responses.Users:
    users_response = responses.Users(
        users=users.users,
        total=users.total,
        offset=users.offset if users.offset is not Empty.UNSET else None,
        limit=users.limit if users.limit is not Empty.UNSET else None,
    )

    return users_response
