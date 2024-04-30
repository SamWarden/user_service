from uuid import UUID

import pytest

from src.application.user.commands import SetUserFullName, SetUserFullNameHandler
from src.application.user.exceptions import UserIdNotExistError
from src.domain.user import User
from src.domain.user.events import FullNameUpdated
from src.domain.user.exceptions import UserIsDeletedError
from src.domain.user.value_objects import FullName, UserId, Username
from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


async def test_set_user_full_name_handler_success(
    user_repo: UserRepoMock,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = SetUserFullNameHandler(user_repo, uow, event_mediator)

    user_id = UserId(UUID("123e4567-e89b-12d3-a456-426614174000"))
    username = Username("john_doe")
    user = User(
        id=user_id,
        username=username,
        full_name=FullName("John", "Doe"),
    )
    await user_repo.add_user(user)

    command = SetUserFullName(
        user_id=user_id.value,
        first_name="John",
        last_name="Smith",
        middle_name=None,
    )

    await handler(command)

    assert user.id == user_id
    assert user.username == username
    assert user.full_name == FullName(command.first_name, command.last_name, command.middle_name)

    assert len(event_mediator.published_events) == 1
    published_event = event_mediator.published_events[0]
    assert isinstance(published_event, FullNameUpdated)
    assert published_event.user_id == command.user_id
    assert published_event.first_name == command.first_name
    assert published_event.last_name == command.last_name
    assert published_event.middle_name == command.middle_name

    assert uow.committed is True


async def test_set_user_full_name_handler_user_not_found(
    user_repo: UserRepoMock,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = SetUserFullNameHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")

    command = SetUserFullName(
        user_id=user_id,
        first_name="John",
        last_name="Smith",
        middle_name=None,
    )

    with pytest.raises(UserIdNotExistError):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False


async def test_set_user_full_name_handler_user_deleted(
    user_repo: UserRepoMock,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
) -> None:
    handler = SetUserFullNameHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    username = Username("john_doe")
    user = User(
        id=UserId(user_id),
        username=username,
        full_name=FullName("John", "Doe"),
        existing_usernames={username},
    )
    user.delete()
    await user_repo.add_user(user)

    command = SetUserFullName(
        user_id=user_id,
        first_name="John",
        last_name="Smith",
        middle_name=None,
    )

    with pytest.raises(UserIsDeletedError):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False
