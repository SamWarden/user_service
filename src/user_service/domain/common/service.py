from abc import ABC

from user_service.domain.common.event import Event


class BaseService(ABC):
    def __init__(self) -> None:
        self._events: list[Event] = []

    def _record_event(self, event: Event) -> None:
        self._events.append(event)

    def get_events(self) -> list[Event]:
        return self._events

    def clear_events(self) -> None:
        self._events.clear()

    def pull_events(self) -> list[Event]:
        events = self.get_events().copy()
        self.clear_events()
        return events
