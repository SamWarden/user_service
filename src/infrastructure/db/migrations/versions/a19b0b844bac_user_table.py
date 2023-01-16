"""User table

Revision ID: a19b0b844bac
Revises: 92cc120d7301
Create Date: 2023-01-16 20:39:09.884944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a19b0b844bac"
down_revision = "92cc120d7301"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), server_default=sa.text("uuid_generate_v7()"), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("deleted", sa.Boolean(), server_default=sa.text("FALSE"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username"))
    )


def downgrade() -> None:
    op.drop_table("users")
