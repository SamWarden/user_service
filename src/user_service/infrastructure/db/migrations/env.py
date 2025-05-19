import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from user_service.infrastructure.config_loader import load_config
from user_service.infrastructure.db import DBConfig
from user_service.infrastructure.db.models.base import BaseModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

if not (FULL_URL := config.get_main_option("sqlalchemy.url")):
    try:
        FULL_URL = load_config(DBConfig, "db").full_url
    except FileNotFoundError:
        FULL_URL = None

TARGET_METADATA = BaseModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=FULL_URL,
        target_metadata=TARGET_METADATA,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=TARGET_METADATA)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations(engine: Engine) -> None:
    with engine.connect() as connection:
        do_run_migrations(connection)

    engine.dispose()


async def run_async_migrations(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


def setup_engine() -> Engine:
    return engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
        url=FULL_URL,
    )


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine or receive a connection
    and associate the connection with the context.
    """
    connection: Connection | None = config.attributes.get("connection", None)
    match connection:
        case None:
            engine = setup_engine()
            if engine.driver == "asyncpg":
                async_engine = AsyncEngine(engine)
                asyncio.run(run_async_migrations(async_engine))
            else:
                run_migrations(engine)
        case Connection():  # type: ignore
            do_run_migrations(connection)  # type: ignore
        case _:
            raise TypeError(f"Unexpected connection type: {type(connection)}. Expected Connection")


def main() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


main()
