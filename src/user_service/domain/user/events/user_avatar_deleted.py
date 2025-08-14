"""User avatar deleted event."""
import dataclasses
from uuid import UUID

from user_service.domain.common.event import Event


@dataclasses.dataclass(frozen=True)
class UserAvatarDeleted(Event):
    """User avatar deleted event."""

    user_id: UUID
