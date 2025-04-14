"""Add "deleted_at" column to the "users" table.

Revision ID: 36112198c668
Revises: adbf32e55780
Create Date: 2023-10-18 14:46:21.884051

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "36112198c668"
down_revision = "adbf32e55780"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("deleted_at", sa.DateTime(), server_default=sa.text("NULL"), nullable=True))
    # set deleted_at to the updated_at value for all existing users
    op.execute("UPDATE users SET deleted_at = updated_at WHERE deleted IS true")
    op.drop_column("users", "deleted")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("deleted", sa.BOOLEAN(), server_default=sa.text("false"), autoincrement=False, nullable=False),
    )
    op.execute("UPDATE users SET deleted = true WHERE deleted_at IS NOT NULL")
    op.drop_column("users", "deleted_at")
