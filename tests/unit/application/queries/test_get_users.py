from datetime import UTC, datetime
from uuid import UUID

import pytest

from src.application.common.pagination.dto import Pagination, SortOrder
from src.application.user import dto
from src.application.user.interfaces.persistence import GetUsersFilters
from src.application.user.queries.get_users import GetUsers, GetUsersHandler
from src.domain.common.constants import Empty
from tests.mocks.user_reader import UserReaderMock


@pytest.fixture()
def users() -> list[dto.UserDTOs]:
    users: list[dto.UserDTOs] = [
        dto.User(
            id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            username="john_doe",
            first_name="John",
            last_name="Doe",
            middle_name=None,
        ),
        dto.DeletedUser(
            id=UUID("123e4567-e89b-12d3-a456-426614174001"),
            first_name="Jane",
            last_name="Smith",
            middle_name=None,
            deleted_at=datetime.now(UTC),
        ),
    ]
    return users


async def test_get_users_handler_success(users: list[dto.UserDTOs], user_reader: UserReaderMock) -> None:
    await user_reader.add_users(users)
    handler = GetUsersHandler(user_reader)

    query = GetUsers(
        filters=GetUsersFilters(deleted=Empty.UNSET),
        pagination=Pagination(
            offset=0,
            limit=10,
            order=SortOrder.DESC,
        ),
    )
    result = await handler(query)

    assert result.data == sorted(users, key=lambda user: user.id, reverse=True)
    assert result.pagination.total == len(users)
    assert result.pagination.offset == query.pagination.offset
    assert result.pagination.limit == query.pagination.limit
    assert result.pagination.order == query.pagination.order


async def test_get_users_handler_no_users(users: list[dto.UserDTOs], user_reader: UserReaderMock) -> None:
    handler = GetUsersHandler(user_reader)
    await user_reader.add_users(users)

    query = GetUsers(
        filters=GetUsersFilters(deleted=False),
        pagination=Pagination(
            offset=0,
            limit=10,
            order=SortOrder.ASC,
        ),
    )
    result = await handler(query)

    assert result.data == [users[0]]
    assert result.pagination.total == 1
    assert result.pagination.offset == query.pagination.offset
    assert result.pagination.limit == query.pagination.limit
    assert result.pagination.order == query.pagination.order
