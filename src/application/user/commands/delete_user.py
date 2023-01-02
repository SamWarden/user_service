from dataclasses import dataclass

from didiator import EventMediator

from src.application.base.command import Command, CommandHandler
from src.application.base.interfaces.mapper import Mapper
from src.application.base.interfaces.uow import UnitOfWork
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user.value_objects import UserId


@dataclass(frozen=True)
class DeleteUser(Command[None]):
    user_id: UserId


class DeleteUserHandler(CommandHandler[DeleteUser, None]):
    def __init__(self, user_repo: UserRepo, uow: UnitOfWork, mapper: Mapper, mediator: EventMediator) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mapper = mapper
        self._mediator = mediator

    async def __call__(self, command: DeleteUser) -> None:
        user = await self._user_repo.get_user_by_id(command.user_id)
        user.delete()
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()
