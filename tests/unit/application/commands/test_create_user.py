from uuid import UUID

import pytest

from src.application.user.commands import CreateUser, CreateUserHandler
from src.domain.user.entities import User
from src.domain.user.events import UserCreated
from src.domain.user.exceptions import UsernameAlreadyExistsError
from src.domain.user.value_objects import FullName, UserId, Username
from src.domain.user.value_objects.deleted_status import DeletionTime
from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


async def test_create_user_handler_success(
    user_repo: UserRepoMock,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = CreateUserHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    command = CreateUser(
        user_id=user_id,
        username="john_doe",
        first_name="John",
        last_name="Doe",
        middle_name=None,
    )

    user_id_result = await handler(command)

    assert user_id == user_id_result
    user = user_repo.users[UserId(user_id)]

    assert user.id == UserId(user_id)
    assert user.username == Username(command.username)
    assert user.full_name == FullName(command.first_name, command.last_name, command.middle_name)
    assert user.deleted_at == DeletionTime(None)

    assert len(event_mediator.published_events) == 1
    published_event = event_mediator.published_events[0]
    assert isinstance(published_event, UserCreated)
    assert published_event.user_id == command.user_id
    assert published_event.username == command.username
    assert published_event.first_name == command.first_name
    assert published_event.last_name == command.last_name
    assert published_event.middle_name == command.middle_name

    assert uow.committed is True
    assert uow.rolled_back is False


async def test_create_user_handler_existing_username(
    user_repo: UserRepoMock,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = CreateUserHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    existing_user = User(
        id=UserId(UUID("123e4567-e89b-12d3-a456-426614174001")),
        username=Username("john_doe"),
        full_name=FullName("John", "Doe"),
    )
    user_repo.users[existing_user.id] = existing_user

    command = CreateUser(
        user_id=user_id,
        username="john_doe",
        first_name="Jane",
        last_name="Smith",
        middle_name=None,
    )

    with pytest.raises(UsernameAlreadyExistsError):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False
