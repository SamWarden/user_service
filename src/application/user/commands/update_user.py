from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.mapper import Mapper
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user import dto, validators
from src.application.user.interfaces import UserRepo
from src.domain.base.constants import Empty
from src.domain.user.value_objects import UserId, Username


@dataclass(frozen=True)
class UpdateUserData:
    username: str | Empty = Empty.UNSET
    first_name: str | Empty = Empty.UNSET
    last_name: str | None | Empty = Empty.UNSET

    def __post_init__(self) -> None:
        if self.username is not Empty.UNSET:
            validators.validate_username(self.username)


@dataclass(frozen=True)
class UpdateUser(Command[dto.User]):
    user_id: UUID
    user_data: UpdateUserData


class UpdateUserHandler(CommandHandler[UpdateUser, dto.User]):
    def __init__(self, user_repo: UserRepo, uow: UnitOfWork, mapper: Mapper, mediator: EventMediator) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mapper = mapper
        self._mediator = mediator

    async def __call__(self, command: UpdateUser) -> dto.User:
        user = await self._user_repo.acquire_user_by_id(UserId(command.user_id))
        username = Username(command.user_data.username) if command.user_data.username is not Empty.UNSET else Empty.UNSET
        user.update(
            username,
            command.user_data.first_name,
            command.user_data.last_name,
        )
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        user_dto = self._mapper.load(user, dto.User)
        return user_dto
