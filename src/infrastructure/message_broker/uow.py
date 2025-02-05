import aio_pika
from aiormq import AMQPError

from src.application.common.exceptions import CommitError, RollbackError
from src.application.common.interfaces.uow import UnitOfWork


class RabbitMQUoW(UnitOfWork):
    def __init__(self, rq_transaction: aio_pika.abc.AbstractTransaction) -> None:
        self._rq_transaction = rq_transaction

    async def commit(self) -> None:
        try:
            await self._rq_transaction.commit()
        except AMQPError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._rq_transaction.rollback()
        except AMQPError as err:
            raise RollbackError from err
