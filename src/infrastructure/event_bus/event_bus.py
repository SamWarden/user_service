import logging

from orjson import orjson

from src.infrastructure.message_broker import Message, MessageBroker
from src.infrastructure.log.processors import additionally_serialize

from .events.base import IntegrationEvent

logger = logging.getLogger(__name__)


class EventBusImpl:
    def __init__(self, message_broker: MessageBroker) -> None:
        self._message_broker = message_broker

    async def publish_event(self, event: IntegrationEvent) -> None:
        message = self.build_message(event)
        await self._message_broker.publish_message(message, event._routing_key, event._exchange_name)
        logger.debug("Event published", extra={"event_data": event})

    async def declare_exchange(self, exchange_name: str) -> None:
        await self._message_broker.declare_exchange(exchange_name)

    @staticmethod
    def build_message(event: IntegrationEvent) -> Message:
        return Message(
            id=event.event_id,
            data=orjson.dumps(event, default=additionally_serialize).decode(),
            message_type="event",
        )
