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


def get_revisions(alembic_config: AlembicConfig) -> list[Script]:
    # Get directory object with Alembic migrations
    revisions_dir = ScriptDirectory(alembic_config.get_main_option("script_location"))

    # Get & sort migrations, from first to last
    revisions: list[Script] = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.fixture(scope="module", autouse=True)
def _drop_db(alembic_config: AlembicConfig) -> None:
    downgrade(alembic_config, "base")


@pytest.mark.order("first")
def test_migrations_stairway(alembic_config: AlembicConfig) -> None:
    for revision in get_revisions(alembic_config):
        upgrade(alembic_config, revision.revision)

        # We need -1 for downgrading first migration (its down_revision is None)
        downgrade(alembic_config, revision.down_revision or "-1")
        upgrade(alembic_config, revision.revision)
