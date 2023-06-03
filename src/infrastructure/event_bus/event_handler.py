from src.application.common.event import EventHandler
from src.application.common.exceptions import MappingError
from src.application.common.interfaces.mapper import Mapper
from src.domain.common.events import Event
from src.infrastructure.event_bus.event_bus import EventBusImpl
from src.infrastructure.event_bus.events import UserCreated, UserDeleted, UserUpdated

IntegrationEvents = UserCreated | UserDeleted | UserUpdated


class EventHandlerPublisher(EventHandler[Event]):
    def __init__(self, event_bus: EventBusImpl, mapper: Mapper) -> None:
        self._event_bus = event_bus
        self._mapper = mapper

    async def __call__(self, event: Event) -> None:
        try:
            integration_event = self._mapper.load(event, IntegrationEvents)  # type: ignore
        except MappingError:
            return
        await self._event_bus.publish_event(integration_event)
