from typing import Any, List, Union

from didiator import Event, EventMediator


class EventMediatorMock(EventMediator):
    def __init__(self):
        self.published_events: List[Event] = []

    async def publish(self, events: Union[Event, List[Event]], *args: Any, **kwargs: Any) -> None:
        if isinstance(events, Event):
            events = [events]
        self.published_events.extend(events)
