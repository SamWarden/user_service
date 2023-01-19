from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interfaces.mapper import Mapper


class SQLAlchemyRepo:
    def __init__(self, session: AsyncSession, mapper: Mapper) -> None:
        self._session = session
        self._mapper = mapper
