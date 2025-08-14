from uuid import UUID

from user_service.application.user.commands import (
    DeleteUserAvatar,
    DeleteUserAvatarHandler,
)
from user_service.domain.user.value_objects import UserId

from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


async def test_delete_user_avatar_handler_success(
    user_repo: UserRepoMock,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
    user_service,
) -> None:
    handler = DeleteUserAvatarHandler(user_service, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")

    command = DeleteUserAvatar(user_id=user_id)

    await handler(command)

    user = await user_repo.acquire_user_by_id(UserId(user_id))

    assert user.avatar_id is None
    assert uow.committed is True
