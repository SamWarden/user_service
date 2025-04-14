from typing import Protocol

from .message import Message


class MessageBroker(Protocol):
    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        raise NotImplementedError

    async def declare_exchange(self, exchange_name: str) -> None:
        raise NotImplementedError
