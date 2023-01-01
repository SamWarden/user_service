import dataclasses

from src.domain.base.events.event import Event
from src.domain.user.value_objects.user_id import UserId


@dataclasses.dataclass(frozen=True)
class UserDeleted(Event):  # noqa
    user_id: UserId
