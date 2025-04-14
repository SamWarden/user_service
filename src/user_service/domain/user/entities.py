import dataclasses

from user_service.domain.common.entity import Entity
from user_service.domain.user.value_objects import FullName, UserId, Username
from user_service.domain.user.value_objects.deletion_time import DeletionTime


@dataclasses.dataclass
class User(Entity):
    id: UserId
    username: Username
    full_name: FullName
    deleted_at: DeletionTime = dataclasses.field(default=DeletionTime.create_not_deleted(), kw_only=True)
