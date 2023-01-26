from di.container import ContainerState
from didiator import Mediator
from fastapi import Depends

from .di import get_di_state


class MediatorProvider:
    def __init__(self, mediator: Mediator) -> None:
        self._mediator = mediator

    async def build(self, di_state: ContainerState = Depends(get_di_state)) -> Mediator:
        mediator = self._mediator.bind(di_state=di_state)
        return mediator
