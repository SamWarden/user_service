from uuid import UUID

from src.application.user import dto
from src.application.user.interfaces.persistence import GetUsersOrder
from src.application.user.queries.get_users import GetUsers, GetUsersHandler
from src.domain.common.constants import Empty
from tests.mocks.user_reader import UserReaderMock


async def test_get_users_handler_success(user_reader: UserReaderMock) -> None:
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
        ),
    ]
    await user_reader.add_users(users)
    handler = GetUsersHandler(user_reader)

    query = GetUsers(
        deleted=Empty.UNSET,
        offset=0,
        limit=10,
        order=GetUsersOrder.DESC,
    )
    result = await handler(query)

    assert result.users == sorted(users, key=lambda user: user.id, reverse=True)
    assert result.total == len(users)
    assert result.offset == query.offset
    assert result.limit == query.limit


async def test_get_users_handler_no_users(user_reader: UserReaderMock) -> None:
    handler = GetUsersHandler(user_reader)
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
        ),
    ]
    await user_reader.add_users(users)

    query = GetUsers(
        deleted=False,
        offset=0,
        limit=10,
        order=GetUsersOrder.ASC,
    )
    result = await handler(query)

    assert result.users == [users[0]]
    assert result.total == 1
    assert result.offset == query.offset
    assert result.limit == query.limit
