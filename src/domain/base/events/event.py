from abc import ABC
from dataclasses import dataclass, field

import didiator

from src.domain.base.value_objects.event_id import EventId
from src.domain.base.value_objects.time import Timestamp


@dataclass(frozen=True)
class Event(didiator.Event, ABC):
    event_id: EventId = field(kw_only=True, default_factory=EventId.generate)
    event_timestamp: Timestamp = field(kw_only=True, default_factory=Timestamp.now)
