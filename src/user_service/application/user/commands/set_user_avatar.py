import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from user_service.application.common.command import Command, CommandHandler
from user_service.application.common.interfaces.uow import UnitOfWork
from user_service.domain.user.service import UserService
from user_service.domain.user.value_objects import AvatarId, UserId

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetUserAvatar(Command[None]):
    user_id: UUID
    avatar_id: UUID


class SetUserAvatarHandler(CommandHandler[SetUserAvatar, None]):
    def __init__(
        self,
        user_service: UserService,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_service = user_service
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetUserAvatar) -> None:
        user_id = UserId(command.user_id)
        avatar_id = AvatarId(command.avatar_id)

        await self._user_service.set_user_avatar(user_id, avatar_id)
        await self._mediator.publish(self._user_service.pull_events())
        await self._uow.commit()

        logger.info(
            "User avatar set",
            extra={"user_id": user_id.to_raw(), "avatar_id": avatar_id.to_raw()},
        )
