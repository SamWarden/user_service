from uuid import UUID

from user_service.application.user.commands import SetUserAvatar, SetUserAvatarHandler
from user_service.domain.user.value_objects import AvatarId, UserId

from tests.mocks import EventMediatorMock, UserRepoMock
from tests.mocks.uow import UnitOfWorkMock


async def test_set_user_avatar_handler_success(
    user_repo: UserRepoMock,
    uow: UnitOfWorkMock,
    event_mediator: EventMediatorMock,
    user_service,
) -> None:
    handler = SetUserAvatarHandler(user_service, uow, event_mediator)

    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    avatar_id = UUID("123e4567-e89b-12d3-a456-426614174001")

    command = SetUserAvatar(user_id=user_id, avatar_id=avatar_id)

    await handler(command)

    user = await user_repo.acquire_user_by_id(UserId(user_id))

    assert user.avatar_id == AvatarId(avatar_id)
    assert uow.committed is True
