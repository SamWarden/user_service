import dataclasses
from uuid import UUID

from user_service.domain.common.event import Event


@dataclasses.dataclass(frozen=True)
class FullNameUpdated(Event):
    user_id: UUID
    first_name: str
    last_name: str
    middle_name: str | None
