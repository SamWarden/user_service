import dataclasses
from uuid import UUID

from user_service.domain.common.event import Event


@dataclasses.dataclass(frozen=True)
class UserDeleted(Event):
    user_id: UUID
