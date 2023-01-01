import dataclasses
from typing import Self

from src.domain.base.entities.aggregate_root import AggregateRoot
from src.domain.base.constants import UNSET
from src.domain.user.events.user_created import UserCreated
from src.domain.user.events.user_deleted import UserDeleted
from src.domain.user.events.user_updated import UserUpdated
from src.domain.user.value_objects.user_id import UserId
from src.domain.user.value_objects.username import Username


@dataclasses.dataclass
class User(AggregateRoot):
    id: UserId
    first_name: str
    last_name: str | None
    username: Username
    deleted: bool = dataclasses.field(init=False, default=False)

    @classmethod
    def create(cls, user_id: UserId, first_name: str, last_name: str | None, username: Username) -> Self:
        user = User(user_id, first_name, last_name, username)
        user.record_event(UserCreated(user_id, first_name, last_name, username))
        return user

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def update(
        self,
        first_name: str = UNSET,
        last_name: str | None = UNSET,
        username: Username = UNSET,
    ) -> None:
        if first_name is not UNSET:
            self.first_name = first_name
        if last_name is not UNSET:
            self.last_name = last_name
        if username is not UNSET:
            self.username = username
        self.record_event(UserUpdated(self.id, self.first_name, self.last_name, self.username))

    def delete(self) -> None:
        self.deleted = True
        self.record_event(UserDeleted(self.id))
