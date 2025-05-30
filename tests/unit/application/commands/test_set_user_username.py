from uuid import UUID

import pytest
from user_service.application.user.commands import SetUserUsername, SetUserUsernameHandler
from user_service.application.user.exceptions import UserIdNotExistError
from user_service.domain.user import User
from user_service.domain.user.events import UsernameUpdated
from user_service.domain.user.exceptions import UserIsDeletedError, UsernameAlreadyExistsError
from user_service.domain.user.service import UserService
from user_service.domain.user.value_objects import DeletionTime, FullName, UserId, Username

from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


async def test_set_user_username_handler_success(
    user_repo: UserRepoMock,
    user_service: UserService,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = SetUserUsernameHandler(user_service, uow, event_mediator)

    user_id = UserId(UUID("123e4567-e89b-12d3-a456-426614174000"))
    old_username = Username("old_username")
    new_username = "new_username"
    full_name = FullName("John", "Doe")
    user = User(
        id=user_id,
        username=old_username,
        full_name=full_name,
    )
    await user_repo.add_user(user)

    command = SetUserUsername(user_id=user_id.value, username=new_username)
    await handler(command)

    assert user.id == user_id
    assert user.username == Username(new_username)
    assert user.full_name == full_name

    assert len(event_mediator.published_events) == 1
    published_event = event_mediator.published_events[0]
    assert isinstance(published_event, UsernameUpdated)
    assert published_event.user_id == user_id.value
    assert published_event.username == new_username

    assert uow.committed is True


async def test_set_user_username_handler_username_exists(
    user_repo: UserRepoMock,
    user_service: UserService,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = SetUserUsernameHandler(user_service, uow, event_mediator)

    user_id = UserId(UUID("123e4567-e89b-12d3-a456-426614174000"))
    old_username = Username("old_username")
    new_username = "new_username"
    full_name = FullName("John", "Doe")
    user = User(
        id=user_id,
        username=old_username,
        full_name=full_name,
    )
    user2 = User(
        id=UserId(UUID("123e4567-e89b-12d3-a456-426614174001")),
        username=Username(new_username),
        full_name=full_name,
    )
    await user_repo.add_user(user)
    await user_repo.add_user(user2)

    command = SetUserUsername(user_id=user_id.value, username=new_username)

    with pytest.raises(UsernameAlreadyExistsError):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False


async def test_set_user_username_handler_user_not_found(
    user_repo: UserRepoMock,
    user_service: UserService,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = SetUserUsernameHandler(user_service, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    new_username = "john_doe"

    command = SetUserUsername(user_id=user_id, username=new_username)

    with pytest.raises(UserIdNotExistError):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False


async def test_set_user_username_handler_user_deleted(
    user_repo: UserRepoMock,
    user_service: UserService,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = SetUserUsernameHandler(user_service, uow, event_mediator)

    user_id = UserId(UUID("123e4567-e89b-12d3-a456-426614174000"))
    new_username = "new_username"
    user = User(
        id=user_id,
        username=Username(None),
        full_name=FullName("John", "Doe"),
        deleted_at=DeletionTime.create_deleted(),
    )
    await user_repo.add_user(user)

    command = SetUserUsername(user_id=user_id.value, username=new_username)

    with pytest.raises(UserIsDeletedError):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False
