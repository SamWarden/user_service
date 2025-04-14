from src.infrastructure.message_broker import MessageBroker

USER_EXCHANGE = "users"


async def declare_exchanges(message_broker: MessageBroker) -> None:
    await message_broker.declare_exchange(USER_EXCHANGE)
