import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces import UserRepo
from src.domain.user.value_objects import UserId, Username

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetUserUsername(Command[None]):
    user_id: UUID
    username: str


class SetUserUsernameHandler(CommandHandler[SetUserUsername, None]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetUserUsername) -> None:
        user_id = UserId(command.user_id)
        username = Username(command.username)

        user = await self._user_repo.acquire_user_by_id(user_id)
        user.set_username(username)
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("Username updated", extra={"user": user})
