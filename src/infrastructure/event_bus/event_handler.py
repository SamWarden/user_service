from src.application.common.event import EventHandler
from src.application.common.exceptions import MappingError
from src.domain.common.events import Event
from src.infrastructure.event_bus.converters import convert_domain_event_to_integration
from src.infrastructure.event_bus.event_bus import EventBusImpl


class EventHandlerPublisher(EventHandler[Event]):
    def __init__(self, event_bus: EventBusImpl) -> None:
        self._event_bus = event_bus

    async def __call__(self, event: Event) -> None:
        try:
            integration_event = convert_domain_event_to_integration(event)
        except MappingError:
            return
        await self._event_bus.publish_event(integration_event)
