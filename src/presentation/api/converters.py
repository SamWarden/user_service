from src.application.user.commands.update_user import UpdateUserData
from src.domain.common.constants import Empty
from src.presentation.api.controllers import requests


def convert_request_to_update_user_command(request: requests.UpdateUserData) -> UpdateUserData:
    return UpdateUserData(
        username=request.get("username", Empty.UNSET),
        first_name=request.get("first_name", Empty.UNSET),
        last_name=request.get("last_name", Empty.UNSET),
    )
