"""Avatar ID value object."""
from uuid import UUID

from src.user_service.domain.common.value_objects import UUIDValueObject


class AvatarId(UUIDValueObject):
    """Avatar ID value object."""

    def __init__(self, value: UUID) -> None:
        """Initialize the Avatar ID value object.

        Args:
            value (UUID): The value of the avatar ID.
        """
        super().__init__(value)
