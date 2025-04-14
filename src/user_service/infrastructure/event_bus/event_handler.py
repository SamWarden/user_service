from user_service.application.common.event import EventHandler
from user_service.application.common.exceptions import MappingError
from user_service.domain.common.events import Event
from user_service.infrastructure.event_bus.converters import convert_domain_event_to_integration
from user_service.infrastructure.event_bus.event_bus import EventBusImpl


class EventHandlerPublisher(EventHandler[Event]):
    def __init__(self, event_bus: EventBusImpl) -> None:
        self._event_bus = event_bus

    async def __call__(self, event: Event) -> None:
        try:
            integration_event = convert_domain_event_to_integration(event)
        except MappingError:
            return
        await self._event_bus.publish_event(integration_event)
