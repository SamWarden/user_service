from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.exceptions import CommitError, RollbackError
from src.application.common.interfaces.uow import UnitOfWork


class SQLAlchemyUoW(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err
