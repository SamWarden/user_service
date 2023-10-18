from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

import didiator
from uuid6 import uuid7


@dataclass(frozen=True)
class Event(didiator.Event, ABC):
    event_id: UUID = field(init=False, kw_only=True, default_factory=uuid7)
    event_timestamp: datetime = field(init=False, kw_only=True, default_factory=datetime.utcnow)
