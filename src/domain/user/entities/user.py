import dataclasses
from typing import Self

from src.domain.common.constants import Empty
from src.domain.common.entities.aggregate_root import AggregateRoot
from src.domain.user.events.user_created import UserCreated
from src.domain.user.events.user_deleted import UserDeleted
from src.domain.user.events.user_updated import UserUpdated
from src.domain.user.exceptions import UserIsDeleted
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
        user = cls(user_id, username, first_name, last_name)
        user.record_event(UserCreated(user_id.to_uuid(), str(username), first_name, last_name))
        return user

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def update(
        self,
        username: Username | Empty = Empty.UNSET,
        first_name: str | Empty = Empty.UNSET,
        last_name: str | None | Empty = Empty.UNSET,
    ) -> None:
        self._validate_not_deleted()

        if username is not Empty.UNSET:
            self.username = username
        if first_name is not Empty.UNSET:
            self.first_name = first_name
        if last_name is not Empty.UNSET:
            self.last_name = last_name
        self.record_event(UserUpdated(self.id.to_uuid(), str(self.username), self.first_name, self.last_name))

    def delete(self) -> None:
        self._validate_not_deleted()

        self.username = None
        self.deleted = True
        self.record_event(UserDeleted(self.id.to_uuid()))

    def _validate_not_deleted(self) -> None:
        if self.deleted:
            raise UserIsDeleted(self.id.to_uuid())
