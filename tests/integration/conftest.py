import logging
import os
from collections.abc import AsyncGenerator, Generator

import orjson
import pytest
import pytest_asyncio
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer("postgres:15-alpine")
    if os.name == "nt":  # TODO: workaround from testcontainers/testcontainers-python#108
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        logger.info("postgres url %s", postgres_url_)
        yield postgres_url_
    finally:
        postgres.stop()


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> AlembicConfig:
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def _upgrade_schema_db(alembic_config: AlembicConfig) -> None:
    upgrade(alembic_config, "head")


@pytest_asyncio.fixture
async def session_factory(postgres_url: str) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    engine = create_async_engine(
        url=postgres_url,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
    )
    session_factory_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )
    yield session_factory_
    await engine.dispose()


@pytest_asyncio.fixture
async def session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session_:
        yield session_
