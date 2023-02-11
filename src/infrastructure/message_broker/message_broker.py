import logging

import aio_pika
from aio_pika.abc import AbstractChannel
from orjson import orjson

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
        exchange = await self._get_exchange(exchange_name)
        await exchange.publish(rq_message, routing_key=routing_key)
        logger.info(f" [x] Sent {rq_message!r}")

    async def declare_exchange(self, exchange_name: str) -> None:
        await self._channel.declare_exchange(exchange_name, aio_pika.ExchangeType.TOPIC)

    @staticmethod
    def build_message(message: Message) -> aio_pika.Message:
        return aio_pika.Message(
            body=orjson.dumps(dict(message_type=message.message_type, data=message.data)),
            message_id=str(message.id),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            headers={},
        )

    async def _get_exchange(self, exchange_name: str) -> aio_pika.abc.AbstractExchange:
        return await self._channel.get_exchange(exchange_name, ensure=False)
