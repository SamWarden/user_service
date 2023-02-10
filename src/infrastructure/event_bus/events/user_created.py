from dataclasses import dataclass
from uuid import UUID

from src.infrastructure.event_bus.exchanges import USER_EXCHANGE

from .base import integration_event, IntegrationEvent


@dataclass(frozen=True)
@integration_event("UserCreated", exchange=USER_EXCHANGE)
class UserCreated(IntegrationEvent):  # noqa
    user_id: UUID
    username: str
    first_name: str
    last_name: str | None
