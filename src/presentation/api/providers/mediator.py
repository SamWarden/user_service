from typing import Any

from di import ScopeState
from didiator import Mediator
from fastapi import Depends

from src.infrastructure.mediator import get_mediator

from .di import get_di_state


class MediatorProvider:
    def __init__(self, mediator: Mediator) -> None:
        self._mediator = mediator

    async def build(self, di_state: ScopeState = Depends(get_di_state)) -> Mediator:
        di_values: dict[Any, Any] = {ScopeState: di_state}
        mediator = self._mediator.bind(di_state=di_state, di_values=di_values)
        di_values |= {get_mediator: mediator}
        return mediator
