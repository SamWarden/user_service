import uuid
from collections.abc import AsyncGenerator, Generator
from typing import cast

import alembic.command
import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy import URL, Connection, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer


class PostgresDbManager:
    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    async def create_database(self, database: str, template: str = "template1") -> None:
        async with self._engine.connect() as connection:
            # "template1" is the default template name for the `CREATE DATABASE` statement
            await connection.execute(text(f'CREATE DATABASE "{database}" ENCODING \'utf8\' TEMPLATE "{template}"'))

    async def drop_database(self, database: str) -> None:
        async with self._engine.connect() as connection:
            await connection.execute(text(f'DROP DATABASE "{database}"'))


@pytest.fixture(scope="session")
def postgres() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer("postgres:17.5", dbname="template-db", driver="asyncpg") as postgres:
        yield postgres


def get_alembic_config() -> AlembicConfig:
    return AlembicConfig(file_="alembic.ini")


def run_migrations(connection: Connection) -> None:
    alembic_config = get_alembic_config()
    alembic_config.attributes["connection"] = connection
    alembic.command.upgrade(config=alembic_config, revision="head")


@pytest.fixture(scope="session")
async def template_db_engine(postgres: PostgresContainer) -> AsyncGenerator[AsyncEngine, None]:
    postgres_url = postgres.get_connection_url()
    engine = create_async_engine(postgres_url)
    async with engine.connect() as connection:
        await connection.run_sync(run_migrations)

    # Connections have to be disposed to allow to use the database as a template
    await engine.dispose()
    yield engine
    await engine.dispose()


@pytest.fixture()
async def test_postgres_url(
    request: pytest.FixtureRequest, template_db_engine: AsyncEngine
) -> AsyncGenerator[URL, None]:
    postgres_engine = create_async_engine(template_db_engine.url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    postgres_db_manager = PostgresDbManager(postgres_engine)
    test_postgres_id = uuid.uuid4().hex
    database_name = f"test-db-{test_postgres_id}"

    try:
        empty_database = request.param.get("empty_database", False)
    except AttributeError:
        empty_database = False

    if empty_database:
        await postgres_db_manager.create_database(database_name)
    else:
        template_name = cast(str, template_db_engine.url.database)
        await postgres_db_manager.create_database(database_name, template=template_name)

    postgres_url = template_db_engine.url.set(database=database_name)
    yield postgres_url

    await postgres_db_manager.drop_database(database_name)
    await postgres_engine.dispose()


@pytest.fixture()
async def engine(test_postgres_url: str) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(test_postgres_url)
    yield engine
    await engine.dispose()


@pytest.fixture()
async def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@pytest.fixture()
async def session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
