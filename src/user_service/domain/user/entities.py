import dataclasses

from user_service.domain.common.entity import Entity
from user_service.domain.user.value_objects import (
    AvatarId,
    FullName,
    UserId,
    Username,
)
from user_service.domain.user.value_objects.deletion_time import DeletionTime


@dataclasses.dataclass
class User(Entity):
    id: UserId
    username: Username
    full_name: FullName
    avatar_id: AvatarId | None = dataclasses.field(kw_only=True, default=None)
    deleted_at: DeletionTime = dataclasses.field(
        default=DeletionTime.create_not_deleted(), kw_only=True
    )
