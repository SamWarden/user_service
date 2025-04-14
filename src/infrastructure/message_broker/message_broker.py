import logging

import aio_pika
import orjson
from aio_pika.abc import AbstractChannel

from .interface import MessageBroker
from .message import Message

logger = logging.getLogger(__name__)


class MessageBrokerImpl(MessageBroker):
    def __init__(self, channel: AbstractChannel) -> None:
        self._channel = channel

    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        rq_message = self.build_message(message)
        await self._publish_message(rq_message, routing_key, exchange_name)

    async def declare_exchange(self, exchange_name: str) -> None:
        await self._channel.declare_exchange(exchange_name, aio_pika.ExchangeType.TOPIC)

    @staticmethod
    def build_message(message: Message) -> aio_pika.Message:
        return aio_pika.Message(
            body=orjson.dumps({"message_type": message.message_type, "data": message.data}),
            message_id=str(message.id),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            headers={},
        )

    async def _publish_message(
        self,
        rq_message: aio_pika.Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        exchange = await self._get_exchange(exchange_name)
        await exchange.publish(rq_message, routing_key=routing_key)
        logger.debug("Message sent", extra={"rq_message": rq_message})

    async def _get_exchange(self, exchange_name: str) -> aio_pika.abc.AbstractExchange:
        return await self._channel.get_exchange(exchange_name, ensure=False)
