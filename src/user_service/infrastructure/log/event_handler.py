import logging

from user_service.application.common.event import EventHandler
from user_service.domain.common.events import Event

logger = logging.getLogger(__name__)


class EventLogger(EventHandler[Event]):
    async def __call__(self, event: Event) -> None:
        logger.info("Event occurred", extra={"event_data": event})
