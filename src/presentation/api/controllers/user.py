from typing import Union
from uuid import UUID

from didiator import CommandMediator, QueryMediator
from fastapi import APIRouter, Depends, Path, Query, status

from src.application.common.interfaces.mapper import Mapper
from src.application.user import dto
from src.application.user.commands import CreateUser, DeleteUser
from src.application.user.commands.update_user import UpdateUser, UpdateUserData
from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameAlreadyExists, UsernameNotExist
from src.application.user.interfaces.persistence import GetUsersOrder
from src.application.user.queries import GetUserById, GetUserByUsername, GetUsers
from src.application.user.validators.username import (
    EmptyUsername, MAX_USERNAME_LENGTH, TooLongUsername, WrongUsernameFormat,
)
from src.domain.common.constants import Empty
from src.domain.user.exceptions import UserIsDeleted
from src.presentation.api.controllers import requests, responses
from src.presentation.api.controllers.responses import ErrorResult
from src.presentation.api.presenter import Presenter
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
            "model": ErrorResult[Union[TooLongUsername, EmptyUsername, WrongUsernameFormat]],
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResult[Union[UsernameAlreadyExists, UserIdAlreadyExists]],
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


@user_router.get(
    "/@{username}",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResult[UsernameNotExist]},
    },
)
async def get_user_by_username(
    username: str = Path(max_length=MAX_USERNAME_LENGTH),
    mediator: QueryMediator = Depends(Stub(QueryMediator)),
) -> dto.User:
    user = await mediator.query(GetUserByUsername(username=username))
    return user


@user_router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": dto.UserDTOs},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResult[UserIdNotExist]},
    },
)
async def get_user_by_id(
    user_id: UUID,
    mediator: QueryMediator = Depends(Stub(QueryMediator)),
) -> dto.UserDTOs:
    user = await mediator.query(GetUserById(user_id=user_id))
    return user


@user_router.get(
    "/", description="Return all users",
)
async def get_users(
    deleted: bool | None = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(1000, ge=0, le=1000),
    order: GetUsersOrder = GetUsersOrder.ASC,
    mediator: QueryMediator = Depends(Stub(QueryMediator)),
    presenter: Presenter = Depends(Stub(Presenter)),
) -> responses.Users:
    users = await mediator.query(GetUsers(
        deleted=deleted if deleted is not None else Empty.UNSET,
        offset=offset,
        limit=limit,
        order=order,
    ))
    return presenter.load(users, responses.Users)


@user_router.patch(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResult[Union[UserIdNotExist, UsernameAlreadyExists]]},
        status.HTTP_409_CONFLICT: {"model": ErrorResult[UserIsDeleted]},
    },
)
async def update_user(
    user_id: UUID,
    update_user_data: requests.UpdateUserData,
    mapper: Mapper = Depends(Stub(Mapper)),
    mediator: CommandMediator = Depends(Stub(CommandMediator)),
) -> dto.User:
    user_data = mapper.load(update_user_data, UpdateUserData)
    user = await mediator.send(UpdateUser(user_id=user_id, user_data=user_data))
    return user


@user_router.delete(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": dto.DeletedUser},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResult[UserIdNotExist]},
        status.HTTP_409_CONFLICT: {"model": ErrorResult[UserIsDeleted]},
    },
)
async def delete_user(
    user_id: UUID,
    mediator: CommandMediator = Depends(Stub(CommandMediator)),
) -> dto.DeletedUser:
    deleted_user = await mediator.send(DeleteUser(user_id=user_id))
    return deleted_user
