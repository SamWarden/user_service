import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces import UserRepo
from src.domain.user.entities import User
from src.domain.user.value_objects import FullName, UserId, Username

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
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateUser) -> UUID:
        user_id = UserId(command.user_id)
        username = Username(command.username)
        full_name = FullName(command.first_name, command.last_name, command.middle_name)

        existing_usernames = await self._user_repo.get_existing_usernames()
        user = User.create(user_id, username, full_name, existing_usernames)
        await self._user_repo.add_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("User created", extra={"user": user})

        return command.user_id
