from .event_bus import EventBusImpl
from .exchanges import USER_EXCHANGE


async def declare_exchanges(event_bus: EventBusImpl) -> None:
    await event_bus.declare_exchange(USER_EXCHANGE)
