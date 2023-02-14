from typing import Sequence

from src.application.common.interfaces.uow import UnitOfWork
from src.infrastructure.db.uow import SQLAlchemyUoW
from src.infrastructure.message_broker.uow import RabbitMQUoW


def build_uow(db_uow: SQLAlchemyUoW, rq_uow: RabbitMQUoW) -> UnitOfWork:
    uow = UnitOfWorkImpl((db_uow, rq_uow))
    return uow


class UnitOfWorkImpl(UnitOfWork):
    def __init__(self, uows: Sequence[UnitOfWork]) -> None:
        self._uows = uows

    async def commit(self) -> None:
        for uow in self._uows:
            await uow.commit()

    async def rollback(self) -> None:
        for uow in self._uows:
            await uow.rollback()
