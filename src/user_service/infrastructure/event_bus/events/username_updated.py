from dataclasses import dataclass
from uuid import UUID

from user_service.infrastructure.event_bus.exchanges import USER_EXCHANGE

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event("UsernameUpdated", exchange=USER_EXCHANGE)
class UsernameUpdated(IntegrationEvent):
    user_id: UUID
    username: str
