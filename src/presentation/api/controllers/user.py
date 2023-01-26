from didiator import CommandMediator
from fastapi import APIRouter, Depends, status

from src.application.user import dto
from src.application.user.commands import CreateUser
from src.presentation.api.providers.stub import Stub

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post(
    "/",

    # responses={
    #     status.HTTP_201_CREATED: {"model": dto.User},
    #     status.HTTP_400_BAD_REQUEST: {
    #         "model": Union[UserAlreadyExistError, AccessLevelNotFoundError]
    #     },
    # },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_command: CreateUser,
    mediator: CommandMediator = Depends(Stub(CommandMediator)),
) -> dto.User:
    user = await mediator.send(create_user_command)
    return user
