from src.application.user import dto
from src.domain.user.entities import User


def convert_user_entity_to_dto(user: User) -> dto.User:
    return dto.User(
        id=user.id.to_uuid(),
        username=str(user.username),
        first_name=user.first_name,
        last_name=user.last_name,
    )
