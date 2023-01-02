from dataclasses import dataclass

from didiator import EventMediator

from src.application.base.command import Command, CommandHandler
from src.application.base.interfaces.mapper import Mapper
from src.application.base.interfaces.uow import UnitOfWork
from src.application.user import dto
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user.entities import User
from src.domain.user.value_objects import UserId, Username


@dataclass(frozen=True)
class CreateUser(Command[dto.User]):
    user_id: UserId
    first_name: str
    last_name: str
    username: Username


class CreateUserHandler(CommandHandler[CreateUser, dto.User]):
    def __init__(self, user_repo: UserRepo, uow: UnitOfWork, mapper: Mapper, mediator: EventMediator) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mapper = mapper
        self._mediator = mediator

    async def __call__(self, command: CreateUser) -> dto.User:
        user = User.create(command.user_id, command.first_name, command.last_name, command.username)
        await self._user_repo.add_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()
        user_dto = self._mapper.convert(user, dto.User)
        return user_dto
