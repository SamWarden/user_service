"""Add middle_name column to "users" table.

Revision ID: adbf32e55780
Revises: f78150d890d1
Create Date: 2023-06-04 08:37:29.784295

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "adbf32e55780"
down_revision = "f78150d890d1"
branch_labels = None
depends_on = None

users_table = sa.table(
    "users",
    sa.column("last_name", sa.String()),
)


def upgrade() -> None:
    op.add_column("users", sa.Column("middle_name", sa.String(), nullable=True))
    op.execute(users_table.update().where(users_table.c.last_name.is_(None)).values(last_name="Unknown"))
    op.alter_column("users", "last_name", existing_type=sa.VARCHAR(), nullable=False)


def downgrade() -> None:
    op.alter_column("users", "last_name", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column("users", "middle_name")
