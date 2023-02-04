import dataclasses
from typing import Self

from src.domain.base.entities.aggregate_root import AggregateRoot
from src.domain.base.constants import UNSET
from src.domain.user.events.user_created import UserCreated
from src.domain.user.events.user_deleted import UserDeleted
from src.domain.user.events.user_updated import UserUpdated
from src.domain.user.exceptions import UserAlreadyDeleted
from src.domain.user.value_objects.user_id import UserId
from src.domain.user.value_objects.username import Username


@dataclasses.dataclass
class User(AggregateRoot):
    id: UserId
    username: Username | None
    first_name: str
    last_name: str | None
    deleted: bool = dataclasses.field(default=False, kw_only=True)

    @classmethod
    def create(cls, user_id: UserId, username: Username, first_name: str, last_name: str | None) -> Self:
        user = User(user_id, username, first_name, last_name)
        user.record_event(UserCreated(user_id, username, first_name, last_name))
        return user

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def update(
        self,
        username: Username = UNSET,
        first_name: str = UNSET,
        last_name: str | None = UNSET,
    ) -> None:
        if username is not UNSET:
            self.username = username
        if first_name is not UNSET:
            self.first_name = first_name
        if last_name is not UNSET:
            self.last_name = last_name
        self.record_event(UserUpdated(self.id, self.username, self.first_name, self.last_name))

    def delete(self) -> None:
        if self.deleted:
            raise UserAlreadyDeleted(self.id.value)

        self.username = None
        self.deleted = True
        self.record_event(UserDeleted(self.id))
