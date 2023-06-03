import dataclasses
from typing import Self

from src.domain.common.entities.aggregate_root import AggregateRoot
from src.domain.user.events import FullNameUpdated
from src.domain.user.events.user_created import UserCreated
from src.domain.user.events.user_deleted import UserDeleted
from src.domain.user.events.username_updated import UsernameUpdated
from src.domain.user.exceptions import UserIsDeleted
from src.domain.user.value_objects import FullName, UserId, Username


@dataclasses.dataclass
class User(AggregateRoot):
    id: UserId
    username: Username | None
    full_name: FullName
    deleted: bool = dataclasses.field(default=False, kw_only=True)

    @classmethod
    def create(cls, user_id: UserId, username: Username, full_name: FullName) -> Self:
        user = cls(user_id, username, full_name)
        user.record_event(
            UserCreated(
                user_id.to_uuid(),
                str(username),
                full_name.first_name,
                full_name.last_name,
                full_name.middle_name,
            )
        )
        return user

    def set_username(self, username: Username) -> None:
        self._validate_not_deleted()

        self.username = username
        self.record_event(UsernameUpdated(self.id.to_uuid(), str(self.username)))

    def set_full_name(self, full_name: FullName) -> None:
        self._validate_not_deleted()

        self.full_name = full_name
        self.record_event(
            FullNameUpdated(
                self.id.to_uuid(),
                self.full_name.first_name,
                self.full_name.last_name,
                self.full_name.middle_name,
            )
        )

    def delete(self) -> None:
        self._validate_not_deleted()

        self.username = None
        self.deleted = True
        self.record_event(UserDeleted(self.id.to_uuid()))

    def _validate_not_deleted(self) -> None:
        if self.deleted:
            raise UserIsDeleted(self.id.to_uuid())
