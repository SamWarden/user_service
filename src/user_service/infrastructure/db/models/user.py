import sqlalchemy as sa
from sqlalchemy.orm import composite
from uuid6 import uuid7

from user_service.domain.user import entities, value_objects as vo

from .base import TimedBaseModel, mapper_registry

USERS_TABLE = sa.Table(
    "users",
    TimedBaseModel.metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=sa.func.uuid_generate_v7()),
    sa.Column("username", sa.String, unique=True),
    sa.Column("first_name", sa.String),
    sa.Column("last_name", sa.String),
    sa.Column("middle_name", sa.String),
    sa.Column("deleted_at", sa.DateTime(timezone=True), server_default=sa.text("NULL"), nullable=True),
)

mapper_registry.map_imperatively(
    entities.User,
    USERS_TABLE,
    properties={
        "id": composite(vo.UserId, USERS_TABLE.c.id),
        "username": composite(vo.Username, USERS_TABLE.c.username),
        "full_name": composite(
            vo.FullName,
            USERS_TABLE.c.first_name,
            USERS_TABLE.c.last_name,
            USERS_TABLE.c.middle_name,
        ),
        "deleted_at": composite(vo.DeletionTime, USERS_TABLE.c.deleted_at),
    },
    column_prefix="_",
)
