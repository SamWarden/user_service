from uuid import UUID

import pytest

from src.application.user import dto
from src.application.user.commands import SetUserUsername, SetUserUsernameHandler
from src.application.user.exceptions import UserIdNotExist, UsernameAlreadyExists
from src.domain.user import User
from src.domain.user.events import UsernameUpdated
from src.domain.user.exceptions import UserIsDeleted
from src.domain.user.value_objects import FullName, UserId, Username
from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


async def test_set_user_username_handler_success(
    user_repo: UserRepoMock, uow: UnitOfWorkMock, event_mediator: EventMediatorMock
) -> None:
    handler = SetUserUsernameHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    username = "john_doe"
    user = User(
        id=UserId(user_id),
        username=None,
        full_name=FullName("John", "Doe"),
    )
    await user_repo.add_user(user)

    command = SetUserUsername(
        user_id=user_id,
        username=username,
    )

    result = await handler(command)

    assert isinstance(result, dto.User)
    assert result.id == user_id
    assert result.username == username
    assert result.first_name == user.full_name.first_name
    assert result.last_name == user.full_name.last_name
    assert result.middle_name == user.full_name.middle_name

    assert len(event_mediator.published_events) == 1
    published_event = event_mediator.published_events[0]
    assert isinstance(published_event, UsernameUpdated)
    assert published_event.user_id == user_id
    assert published_event.username == username

    assert uow.committed is True


async def test_set_user_username_handler_username_exists(
    user_repo: UserRepoMock, uow: UnitOfWorkMock, event_mediator: EventMediatorMock
) -> None:
    handler = SetUserUsernameHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    username = "john_doe"
    user = User(
        id=UserId(user_id),
        username=Username(username),
        full_name=FullName("John", "Doe"),
    )
    await user_repo.add_user(user)

    command = SetUserUsername(
        user_id=user_id,
        username=username,
    )

    with pytest.raises(UsernameAlreadyExists):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False


async def test_set_user_username_handler_user_not_found(
    user_repo: UserRepoMock, uow: UnitOfWorkMock, event_mediator: EventMediatorMock
) -> None:
    handler = SetUserUsernameHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    username = "john_doe"

    command = SetUserUsername(
        user_id=user_id,
        username=username,
    )

    with pytest.raises(UserIdNotExist):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False


async def test_set_user_username_handler_user_deleted(
    user_repo: UserRepoMock, uow: UnitOfWorkMock, event_mediator: EventMediatorMock
) -> None:
    handler = SetUserUsernameHandler(user_repo, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    username = "john_doe"
    user = User(
        id=UserId(user_id),
        username=None,
        full_name=FullName("John", "Doe"),
    )
    user.delete()
    await user_repo.add_user(user)

    command = SetUserUsername(
        user_id=user_id,
        username=username,
    )

    with pytest.raises(UserIsDeleted):
        await handler(command)

    assert len(event_mediator.published_events) == 0
    assert uow.committed is False
    assert uow.rolled_back is False
