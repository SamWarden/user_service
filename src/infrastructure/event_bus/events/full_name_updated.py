from dataclasses import dataclass
from uuid import UUID

from src.infrastructure.event_bus.exchanges import USER_EXCHANGE

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event("UsernameUpdated", exchange=USER_EXCHANGE)
class FullNameUpdated(IntegrationEvent):
    user_id: UUID
    first_name: str
    last_name: str
    middle_name: str | None
