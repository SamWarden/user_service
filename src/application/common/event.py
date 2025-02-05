from abc import ABC
from typing import Generic, TypeVar

import didiator

from src.domain.common.events.event import Event

E = TypeVar("E", bound=Event)


class EventHandler(didiator.EventHandler[E], ABC, Generic[E]):
    pass
