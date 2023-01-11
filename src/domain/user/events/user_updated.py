import dataclasses

from src.domain.base.events.event import Event
from src.domain.user.value_objects.user_id import UserId
from src.domain.user.value_objects.username import Username


@dataclasses.dataclass(frozen=True)
class UserUpdated(Event):  # noqa
    user_id: UserId
    username: Username
    first_name: str
    last_name: str | None
