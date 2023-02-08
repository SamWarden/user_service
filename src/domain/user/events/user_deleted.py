import dataclasses
from uuid import UUID

from src.domain.base.events.event import Event


@dataclasses.dataclass(frozen=True)
class UserDeleted(Event):  # noqa
    user_id: UUID
