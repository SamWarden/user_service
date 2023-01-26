from collections.abc import AsyncGenerator

from di.container import ContainerState
from didiator.utils.di_builder import DiBuilder
from fastapi import Depends

from src.infrastructure.constants import REQUEST_SCOPE


def get_di_builder() -> DiBuilder:
    raise NotImplementedError


def get_di_state() -> ContainerState:
    raise NotImplementedError


class StateProvider:
    def __init__(self, di_state: ContainerState | None = None):
        self._di_state = di_state

    async def build(
        self, di_builder: DiBuilder = Depends(get_di_builder),
    ) -> AsyncGenerator[[DiBuilder], ContainerState]:
        async with di_builder.enter_scope(REQUEST_SCOPE, self._di_state) as di_state:
            yield di_state
