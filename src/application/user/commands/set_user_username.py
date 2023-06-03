import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user import dto
from src.application.user.converters import convert_active_user_entity_to_dto
from src.application.user.exceptions import UsernameAlreadyExists
from src.application.user.interfaces import UserRepo
from src.domain.user.value_objects import UserId, Username

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetUserUsername(Command[dto.User]):
    user_id: UUID
    username: str


class SetUserUsernameHandler(CommandHandler[SetUserUsername, dto.User]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetUserUsername) -> dto.User:
        user_id = UserId(command.user_id)
        username = Username(command.username)

        if await self._user_repo.check_username_exists(username):
            raise UsernameAlreadyExists(str(username))

        user = await self._user_repo.acquire_user_by_id(user_id)
        user.set_username(Username(command.username))
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("Username updated", extra={"user": user})

        user_dto = convert_active_user_entity_to_dto(user)
        return user_dto
