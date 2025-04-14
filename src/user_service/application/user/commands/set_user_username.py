import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from user_service.application.common.command import Command, CommandHandler
from user_service.application.common.interfaces.uow import UnitOfWork
from user_service.domain.user.service import UserService
from user_service.domain.user.value_objects import UserId, Username

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetUserUsername(Command[None]):
    user_id: UUID
    username: str


class SetUserUsernameHandler(CommandHandler[SetUserUsername, None]):
    def __init__(
        self,
        user_service: UserService,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_service = user_service
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetUserUsername) -> None:
        user_id = UserId(command.user_id)
        username = Username(command.username)

        await self._user_service.set_user_username(user_id, username)
        await self._mediator.publish(self._user_service.pull_events())
        await self._uow.commit()

        logger.info("Username updated", extra={"user_id": user_id.to_raw(), "username": username.to_raw()})
