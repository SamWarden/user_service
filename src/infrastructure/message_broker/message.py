from dataclasses import dataclass, field
from uuid import UUID

from uuid6 import uuid7


@dataclass(frozen=True, kw_only=True)
class Message:
    id: UUID = field(default_factory=uuid7)
    data: str = ""
    message_type: str = "message"
