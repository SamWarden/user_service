from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.mapper import Mapper
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user import dto
from src.application.user.interfaces import UserRepo
from src.domain.user.value_objects import UserId


@dataclass(frozen=True)
class DeleteUser(Command[dto.DeletedUser]):
    user_id: UUID


class DeleteUserHandler(CommandHandler[DeleteUser, dto.DeletedUser]):
    def __init__(self, user_repo: UserRepo, uow: UnitOfWork, mapper: Mapper, mediator: EventMediator) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mapper = mapper
        self._mediator = mediator

    async def __call__(self, command: DeleteUser) -> dto.DeletedUser:
        user = await self._user_repo.acquire_user_by_id(UserId(command.user_id))
        user.delete()
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        user_dto = self._mapper.load(user, dto.DeletedUser)
        return user_dto
