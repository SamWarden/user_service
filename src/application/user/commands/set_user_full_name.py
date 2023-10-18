import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user import dto
from src.application.user.interfaces import UserRepo
from src.domain.user.value_objects import FullName, UserId

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetUserFullName(Command[dto.User]):
    user_id: UUID
    first_name: str
    last_name: str
    middle_name: str | None


class SetUserFullNameHandler(CommandHandler[SetUserFullName, None]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetUserFullName) -> None:
        user_id = UserId(command.user_id)
        full_name = FullName(command.first_name, command.last_name, command.middle_name)

        user = await self._user_repo.acquire_user_by_id(user_id)
        user.set_full_name(full_name)
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("Full name updated", extra={"user": user})
