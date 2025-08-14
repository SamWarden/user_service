from pydantic import BaseModel
from uuid import UUID

class SetUserAvatarData(BaseModel):
    avatar_id: UUID
