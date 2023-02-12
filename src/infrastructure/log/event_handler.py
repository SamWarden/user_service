import logging

from src.application.common.event import EventHandler
from src.domain.common.events import Event

logger = logging.getLogger(__name__)


class EventLogger(EventHandler[Event]):
    async def __call__(self, event: Event) -> None:
        logger.info("Event occurred", extra={"event_data": event})
