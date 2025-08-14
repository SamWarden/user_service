"""User avatar updated event."""
import dataclasses
from uuid import UUID

from user_service.domain.common.event import Event


@dataclasses.dataclass(frozen=True)
class UserAvatarUpdated(Event):
    """User avatar updated event."""

    user_id: UUID
    avatar_id: UUID
