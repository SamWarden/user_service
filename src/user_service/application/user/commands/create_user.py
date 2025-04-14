import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from user_service.application.common.command import Command, CommandHandler
from user_service.application.common.interfaces.uow import UnitOfWork
from user_service.domain.user.service import UserService
from user_service.domain.user.value_objects import FullName, UserId, Username

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateUser(Command[UUID]):
    user_id: UUID
    username: str
    first_name: str
    last_name: str
    middle_name: str | None


class CreateUserHandler(CommandHandler[CreateUser, UUID]):
    def __init__(
        self,
        user_service: UserService,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_service = user_service
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateUser) -> UUID:
        user_id = UserId(command.user_id)
        username = Username(command.username)
        full_name = FullName(command.first_name, command.last_name, command.middle_name)

        user = await self._user_service.create_user(user_id, username, full_name)
        await self._mediator.publish(self._user_service.pull_events())
        await self._uow.commit()

        logger.info("User created", extra={"user_id": user.id.to_raw(), "user": user})

        return user.id.to_raw()
