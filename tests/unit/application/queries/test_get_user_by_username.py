from uuid import UUID

import pytest
from user_service.application.user import dto
from user_service.application.user.exceptions import UsernameNotExistError
from user_service.application.user.queries.get_user_by_username import GetUserByUsername, GetUserByUsernameHandler

from tests.mocks.user_reader import UserReaderMock


async def test_get_user_by_username_handler_success(user_reader: UserReaderMock) -> None:
    username = "john_doe"
    user = dto.User(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        username=username,
        first_name="John",
        last_name="Doe",
        middle_name=None,
        deleted_at=None,
    )
    await user_reader.add_user(user)
    handler = GetUserByUsernameHandler(user_reader)

    query = GetUserByUsername(username=username)
    result = await handler(query)

    assert result == user


async def test_get_user_by_username_handler_user_not_found(user_reader: UserReaderMock) -> None:
    username = "john_doe"
    user = dto.User(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        username=username,
        first_name="John",
        last_name="Doe",
        middle_name=None,
        deleted_at=None,
    )
    await user_reader.add_user(user)
    handler = GetUserByUsernameHandler(user_reader)

    non_existent_username = "non_existent"
    query = GetUserByUsername(username=non_existent_username)

    with pytest.raises(UsernameNotExistError):
        await handler(query)
