from uuid import UUID

import pytest

from src.application.user import dto
from src.application.user.exceptions import UserIdNotExistError
from src.application.user.queries.get_user_by_id import GetUserById, GetUserByIdHandler
from tests.mocks.user_reader import UserReaderMock


async def test_get_user_by_id_handler(user_reader: UserReaderMock) -> None:
    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    user = dto.User(
        id=user_id,
        username="john_doe",
        first_name="John",
        last_name="Doe",
        middle_name=None,
    )
    await user_reader.add_user(user)
    handler = GetUserByIdHandler(user_reader)

    query = GetUserById(user_id=user_id)
    result = await handler(query)

    assert result == user


async def test_get_user_by_id_handler_user_not_found(user_reader: UserReaderMock) -> None:
    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    user = dto.User(
        id=user_id,
        username="john_doe",
        first_name="John",
        last_name="Doe",
        middle_name=None,
    )
    await user_reader.add_user(user)
    handler = GetUserByIdHandler(user_reader)

    non_existent_user_id = UUID("00000000-0000-0000-0000-000000000000")
    query = GetUserById(user_id=non_existent_user_id)

    with pytest.raises(UserIdNotExistError):
        await handler(query)
