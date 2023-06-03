from typing import Annotated, Union
from uuid import UUID

from didiator import CommandMediator, QueryMediator
from fastapi import APIRouter, Depends, Query, status

from src.application.user import dto
from src.application.user.commands import CreateUser, DeleteUser, SetUserFullName
from src.application.user.commands.set_user_username import SetUserUsername
from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameAlreadyExists, UsernameNotExist
from src.application.user.interfaces.persistence import GetUsersOrder
from src.application.user.queries import GetUserById, GetUserByUsername, GetUsers
from src.domain.common.constants import Empty
from src.domain.user.exceptions import UserIsDeleted
from src.domain.user.value_objects.username import EmptyUsername, TooLongUsername, WrongUsernameFormat
from src.presentation.api.controllers import requests, responses
from src.presentation.api.controllers.responses import ErrorResult
from src.presentation.api.converters import convert_dto_to_users_response
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
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_command: CreateUser,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
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
    username: str,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
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
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> dto.UserDTOs:
    user = await mediator.query(GetUserById(user_id=user_id))
    return user


@user_router.get(
    "/",
    description="Return all users",
)
async def get_users(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    deleted: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=1000)] = 1000,
    order: GetUsersOrder = GetUsersOrder.ASC,
) -> responses.Users:
    users = await mediator.query(
        GetUsers(
            deleted=deleted if deleted is not None else Empty.UNSET,
            offset=offset,
            limit=limit,
            order=order,
        )
    )
    return convert_dto_to_users_response(users)


@user_router.post(
    "/{user_id}/username",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResult[Union[UserIdNotExist, UsernameAlreadyExists]]},
        status.HTTP_409_CONFLICT: {"model": ErrorResult[UserIsDeleted]},
    },
)
async def set_user_username(
    user_id: UUID,
    set_user_username_data: requests.SetUserUsernameData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> dto.User:
    set_user_username_command = SetUserUsername(user_id=user_id, username=set_user_username_data.username)
    user = await mediator.send(set_user_username_command)
    return user


@user_router.post(
    "/{user_id}/full-name",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResult[Union[UserIdNotExist]]},
        status.HTTP_409_CONFLICT: {"model": ErrorResult[UserIsDeleted]},
    },
)
async def set_user_full_name(
    user_id: UUID,
    set_user_full_name_data: requests.SetUserFullNameData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> dto.User:
    set_user_full_name_command = SetUserFullName(
        user_id=user_id,
        first_name=set_user_full_name_data.first_name,
        last_name=set_user_full_name_data.last_name,
        middle_name=set_user_full_name_data.middle_name,
    )
    user = await mediator.send(set_user_full_name_command)
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
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> dto.DeletedUser:
    deleted_user = await mediator.send(DeleteUser(user_id=user_id))
    return deleted_user
