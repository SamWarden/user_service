from dataclasses import dataclass
from uuid import UUID

from src.infrastructure.event_bus.exchanges import USER_EXCHANGE

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event("UserCreated", exchange=USER_EXCHANGE)
class UserCreated(IntegrationEvent):
    user_id: UUID
    username: str
    first_name: str
    last_name: str | None
