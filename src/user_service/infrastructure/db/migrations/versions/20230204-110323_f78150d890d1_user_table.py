"""User table.

Revision ID: f78150d890d1
Revises: 2d79505fb3d2
Create Date: 2023-02-04 11:03:23.887827

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f78150d890d1"
down_revision = "2d79505fb3d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), server_default=sa.func.uuid_generate_v7(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("deleted", sa.Boolean(), server_default=sa.False_(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )


def downgrade() -> None:
    op.drop_table("users")
