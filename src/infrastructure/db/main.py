from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from .config import DBConfig


async def build_sa_engine(db_config: DBConfig) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        db_config.full_url, echo_pool=db_config.echo, future=False,
    )
    yield engine

    await engine.dispose()


def build_sa_session_factory(engine: AsyncEngine) -> sessionmaker:
    session_factory = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
    return session_factory


async def build_sa_session(session_factory: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
