import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user import dto
from src.application.user.converters import convert_deleted_user_entity_to_dto
from src.application.user.interfaces import UserRepo
from src.domain.user.value_objects import UserId

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeleteUser(Command[dto.DeletedUser]):
    user_id: UUID


class DeleteUserHandler(CommandHandler[DeleteUser, dto.DeletedUser]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: DeleteUser) -> dto.DeletedUser:
        user = await self._user_repo.acquire_user_by_id(UserId(command.user_id))
        user.delete()
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("User deleted", extra={"user": user})

        user_dto = convert_deleted_user_entity_to_dto(user)
        return user_dto
