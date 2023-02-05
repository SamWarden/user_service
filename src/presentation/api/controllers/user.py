from didiator import CommandMediator, QueryMediator
from fastapi import APIRouter, Depends, status

from src.application.user import dto
from src.application.user.commands import CreateUser
from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameAlreadyExists
from src.application.user.queries import GetUserById
from src.domain.user.value_objects.username import EmptyUsername, TooLongUsername, WrongUsernameFormat
from src.presentation.api.providers.stub import Stub

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": TooLongUsername | EmptyUsername | WrongUsernameFormat,
        },
        status.HTTP_409_CONFLICT: {
            "model": UsernameAlreadyExists | UserIdAlreadyExists,
        }
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_command: CreateUser,
    mediator: CommandMediator = Depends(Stub(CommandMediator)),
) -> dto.User:
    user = await mediator.send(create_user_command)
    return user
