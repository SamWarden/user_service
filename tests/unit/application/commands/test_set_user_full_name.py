from uuid import UUID

import pytest

from src.application.user import dto
from src.application.user.commands import SetUserFullName, SetUserFullNameHandler
from src.application.user.exceptions import UserIdNotExist
from src.domain.user import User
from src.domain.user.events import FullNameUpdated
from src.domain.user.exceptions import UserIsDeleted
from src.domain.user.value_objects import FullName, UserId, Username
from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


async def test_set_user_full_name_handler_success(
    user_repo: UserRepoMock, uow: UnitOfWorkMock, event_mediator: EventMediatorMock
) -> None:
    handler = SetUserFullNameHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    user = User(
        id=UserId(user_id),
        username=Username("john_doe"),
        full_name=FullName("John", "Doe"),
    )
    user_repo.users[user.id] = user

    command = SetUserFullName(
        user_id=user_id,
        first_name="John",
        last_name="Smith",
        middle_name=None,
    )

    result = await handler(command)

    assert isinstance(result, dto.User)
    assert result.id == user_id
    assert result.username == str(user.username)
    assert result.first_name == command.first_name
    assert result.last_name == command.last_name
    assert result.middle_name == command.middle_name

    assert len(event_mediator.published_events) == 1
    published_event = event_mediator.published_events[0]
    assert isinstance(published_event, FullNameUpdated)
    assert published_event.user_id == user_id
    assert published_event.first_name == command.first_name
    assert published_event.last_name == command.last_name
    assert published_event.middle_name == command.middle_name

    assert uow.committed is True


async def test_set_user_full_name_handler_user_not_found(
    user_repo: UserRepoMock, uow: UnitOfWorkMock, event_mediator: EventMediatorMock
) -> None:
    handler = SetUserFullNameHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")

    command = SetUserFullName(
        user_id=user_id,
        first_name="John",
        last_name="Smith",
        middle_name=None,
    )

    with pytest.raises(UserIdNotExist):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False


async def test_set_user_full_name_handler_user_deleted(
    user_repo: UserRepoMock, uow: UnitOfWorkMock, event_mediator: EventMediatorMock
) -> None:
    handler = SetUserFullNameHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    user = User(
        id=UserId(user_id),
        username=Username("john_doe"),
        full_name=FullName("John", "Doe"),
    )
    user.delete()
    user_repo.users[user.id] = user

    command = SetUserFullName(
        user_id=user_id,
        first_name="John",
        last_name="Smith",
        middle_name=None,
    )

    with pytest.raises(UserIsDeleted):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False
