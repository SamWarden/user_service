import dataclasses
from abc import ABC

import didiator

from src.domain.base.value_objects.event_id import EventId
from src.domain.base.value_objects.time import Timestamp


@dataclasses.dataclass(frozen=True)
class Event(didiator.Event, ABC):
    event_id: EventId = dataclasses.field(kw_only=True, default_factory=EventId.generate)
    event_timestamp: Timestamp = dataclasses.field(kw_only=True, default_factory=Timestamp.now)
