from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker, AsyncEngine, AsyncSession, create_async_engine,
)

from .config import DBConfig


async def build_sa_engine(db_config: DBConfig) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        db_config.full_url, echo_pool=db_config.echo, future=False,
    )
    yield engine

    await engine.dispose()


def build_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    return session_factory


async def build_sa_session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
