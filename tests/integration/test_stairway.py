"""
Test can find forgotten downgrade methods, undeleted data types in downgrade.

methods, typos and many other errors.
Does not require any maintenance - you just add it once to check 80% of typos
and mistakes in migrations forever.
https://github.com/alvassin/alembic-quickstart
"""

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from alembic.script import Script, ScriptDirectory
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import AsyncSession

from tests.fixtures.db import get_alembic_config


def get_revisions(alembic_config: AlembicConfig) -> list[Script]:
    # Get directory object with Alembic migrations
    revisions_dir = ScriptDirectory.from_config(alembic_config)

    # Get & sort migrations, from first to last
    revisions: list[Script] = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


def run_revisions(connection: Connection) -> None:
    alembic_config = get_alembic_config()
    alembic_config.attributes["connection"] = connection
    for revision in get_revisions(alembic_config):
        upgrade(alembic_config, revision.revision)

        # We need -1 for downgrading first migration (its down_revision is None)
        downgrade(alembic_config, revision.down_revision or "-1")
        upgrade(alembic_config, revision.revision)


@pytest.mark.order("first")
async def test_migrations_stairway(session: AsyncSession) -> None:
    connection = await session.connection()
    await connection.run_sync(run_revisions)
