from typing import Protocol


class UnitOfWork(Protocol):
    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError
