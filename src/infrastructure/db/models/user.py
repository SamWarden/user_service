from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from .base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"
    __mapper_args__: ClassVar[dict[Any, Any]] = {"eager_defaults": True}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7, server_default=sa.func.uuid_generate_v7())
    username: Mapped[str | None] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str | None]
    deleted_at: Mapped[datetime | None] = mapped_column(default=None, server_default=sa.Null())
