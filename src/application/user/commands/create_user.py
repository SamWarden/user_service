import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user import dto, validators
from src.application.user.converters import convert_active_user_entity_to_dto
from src.application.user.interfaces import UserRepo
from src.domain.user.entities import User
from src.domain.user.value_objects import UserId, Username

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateUser(Command[dto.User]):
    user_id: UUID
    username: str
    first_name: str
    last_name: str | None

    def __post_init__(self) -> None:
        validators.validate_username(self.username)


class CreateUserHandler(CommandHandler[CreateUser, dto.User]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateUser) -> dto.User:
        user = User.create(
            UserId(command.user_id),
            Username(command.username),
            command.first_name,
            command.last_name,
        )
        await self._user_repo.add_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("User created", extra={"user": user})

        user_dto = convert_active_user_entity_to_dto(user)
        return user_dto
