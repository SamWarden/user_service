from typing import Annotated
from uuid import UUID

from didiator import CommandMediator, Mediator, QueryMediator
from fastapi import APIRouter, Depends, Query, status

from src.application.common.pagination.dto import Pagination, SortOrder
from src.application.user import dto
from src.application.user.commands import CreateUser, DeleteUser, SetUserFullName
from src.application.user.commands.set_user_username import SetUserUsername
from src.application.user.exceptions import UserIdAlreadyExistsError, UserIdNotExistError, UsernameNotExistError
from src.application.user.interfaces.persistence import GetUsersFilters
from src.application.user.queries import GetUserById, GetUserByUsername, GetUsers
from src.domain.common.constants import Empty
from src.domain.user.exceptions import UserIsDeletedError, UsernameAlreadyExistsError
from src.domain.user.value_objects.full_name import EmptyNameError, TooLongNameError, WrongNameFormatError
from src.domain.user.value_objects.username import EmptyUsernameError, TooLongUsernameError, WrongUsernameFormatError
from src.presentation.api.controllers import requests
from src.presentation.api.controllers.responses import ErrorResponse
from src.presentation.api.controllers.responses.base import OkResponse
from src.presentation.api.providers.stub import Stub

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[TooLongUsernameError | EmptyUsernameError | WrongUsernameFormatError],
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[UsernameAlreadyExistsError | UserIdAlreadyExistsError],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_command: CreateUser,
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
) -> OkResponse[dto.UserDTOs]:
    user_id = await mediator.send(create_user_command)
    user = await mediator.query(GetUserById(user_id=user_id))
    return OkResponse(result=user)


@user_router.get(
    "/@{username}",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UsernameNotExistError]},
    },
)
async def get_user_by_username(
    username: str,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> OkResponse[dto.User]:
    user = await mediator.query(GetUserByUsername(username=username))
    return OkResponse(result=user)


@user_router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": dto.UserDTOs},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserIdNotExistError]},
    },
)
async def get_user_by_id(
    user_id: UUID,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> OkResponse[dto.UserDTOs]:
    user = await mediator.query(GetUserById(user_id=user_id))
    return OkResponse(result=user)


@user_router.get(
    "",
)
async def get_users(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    deleted: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
) -> OkResponse[dto.Users]:
    """Return all users."""
    users = await mediator.query(
        GetUsers(
            filters=GetUsersFilters(deleted if deleted is not None else Empty.UNSET),
            pagination=Pagination(
                offset=offset,
                limit=limit,
                order=order,
            ),
        ),
    )
    return OkResponse(result=users)


@user_router.put(
    "/{user_id}/username",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[
                UserIdNotExistError | TooLongUsernameError | EmptyUsernameError | WrongUsernameFormatError
            ],
        },
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeletedError | UsernameAlreadyExistsError]},
    },
)
async def set_user_username(
    user_id: UUID,
    set_user_username_data: requests.SetUserUsernameData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    set_user_username_command = SetUserUsername(user_id=user_id, username=set_user_username_data.username)
    await mediator.send(set_user_username_command)
    return OkResponse()


@user_router.put(
    "/{user_id}/full-name",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[UserIdNotExistError | EmptyNameError | WrongNameFormatError | TooLongNameError],
        },
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeletedError]},
    },
)
async def set_user_full_name(
    user_id: UUID,
    set_user_full_name_data: requests.SetUserFullNameData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    set_user_full_name_command = SetUserFullName(
        user_id=user_id,
        first_name=set_user_full_name_data.first_name,
        last_name=set_user_full_name_data.last_name,
        middle_name=set_user_full_name_data.middle_name,
    )
    await mediator.send(set_user_full_name_command)
    return OkResponse()


@user_router.delete(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": dto.DeletedUser},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserIdNotExistError]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeletedError]},
    },
)
async def delete_user(
    user_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(DeleteUser(user_id=user_id))
    return OkResponse()
