import dataclasses
from uuid import UUID

from src.domain.base.events.event import Event


@dataclasses.dataclass(frozen=True)
class UserUpdated(Event):  # noqa
    user_id: UUID
    username: str
    first_name: str
    last_name: str | None
