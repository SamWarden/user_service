from uuid import UUID

import pytest
from user_service.application.user.commands import DeleteUser, DeleteUserHandler
from user_service.application.user.exceptions import UserIdNotExistError
from user_service.domain.user import User
from user_service.domain.user.events import UserDeleted
from user_service.domain.user.exceptions import UserIsDeletedError
from user_service.domain.user.service import UserService
from user_service.domain.user.value_objects import FullName, UserId, Username
from user_service.domain.user.value_objects.deletion_time import DeletionTime

from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


async def test_delete_user_handler_success(
    user_repo: UserRepoMock,
    user_service: UserService,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = DeleteUserHandler(user_service, uow, event_mediator)

    user_id = UserId(UUID("123e4567-e89b-12d3-a456-426614174000"))
    username = Username("john_doe")
    full_name = FullName("John", "Doe")
    user = User(
        id=user_id,
        username=username,
        full_name=full_name,
        deleted_at=DeletionTime.create_not_deleted(),
    )
    await user_repo.add_user(user)

    command = DeleteUser(user_id=user_id.value)
    await handler(command)

    assert user.id == user_id
    assert user.username == Username(None)
    assert user.full_name == full_name
    assert user.deleted_at != DeletionTime.create_not_deleted()

    assert len(event_mediator.published_events) == 1
    published_event = event_mediator.published_events[0]
    assert isinstance(published_event, UserDeleted)
    assert published_event.user_id == user_id.value

    assert uow.committed is True


async def test_delete_user_handler_user_not_found(
    user_repo: UserRepoMock,
    user_service: UserService,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = DeleteUserHandler(user_service, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")

    command = DeleteUser(user_id=user_id)

    with pytest.raises(UserIdNotExistError):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False


async def test_delete_user_handler_user_already_deleted(
    user_repo: UserRepoMock,
    user_service: UserService,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = DeleteUserHandler(user_service, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    user = User(
        id=UserId(user_id),
        username=Username(None),
        full_name=FullName("John", "Doe"),
        deleted_at=DeletionTime.create_deleted(),
    )
    await user_repo.add_user(user)

    command = DeleteUser(user_id=user_id)

    with pytest.raises(UserIsDeletedError):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False
