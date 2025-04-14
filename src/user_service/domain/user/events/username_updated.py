import dataclasses
from uuid import UUID

from user_service.domain.common.events.event import Event


@dataclasses.dataclass(frozen=True)
class UsernameUpdated(Event):
    user_id: UUID
    username: str
