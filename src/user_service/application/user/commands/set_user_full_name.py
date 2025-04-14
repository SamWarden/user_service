import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from user_service.application.common.command import Command, CommandHandler
from user_service.application.common.interfaces.uow import UnitOfWork
from user_service.application.user import dto
from user_service.domain.user.service import UserService
from user_service.domain.user.value_objects import FullName, UserId

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
        user_service: UserService,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_service = user_service
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetUserFullName) -> None:
        user_id = UserId(command.user_id)
        full_name = FullName(command.first_name, command.last_name, command.middle_name)

        await self._user_service.set_user_full_name(user_id, full_name)
        await self._mediator.publish(self._user_service.pull_events())
        await self._uow.commit()

        logger.info("Full name updated", extra={"user_id": user_id.to_raw(), "full_name": str(full_name)})
