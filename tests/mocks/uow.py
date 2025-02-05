from src.application.common.interfaces.uow import UnitOfWork


class UnitOfWorkMock(UnitOfWork):
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    async def commit(self) -> None:
        if self.rolled_back:
            raise ValueError("Cannot commit after rolling back.")
        self.committed = True

    async def rollback(self) -> None:
        if self.committed:
            raise ValueError("Cannot rollback after committing.")
        self.rolled_back = True
