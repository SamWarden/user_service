from typing import Any

from didiator import Event, EventMediator


class EventMediatorMock(EventMediator):
    def __init__(self) -> None:
        self.published_events: list[Event] = []

    async def publish(self, events: Event | list[Event], *args: Any, **kwargs: Any) -> None:
        if isinstance(events, Event):
            events = [events]
        self.published_events.extend(events)
