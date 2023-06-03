from src.application.common.exceptions import MappingError
from src.application.user import dto
from src.domain.user import entities


def convert_active_user_entity_to_dto(user: entities.User) -> dto.User:
    if user.deleted:
        raise MappingError(f"User {user} is deleted")

    return dto.User(
        id=user.id.to_uuid(),
        username=str(user.username),
        first_name=user.first_name,
        last_name=user.last_name,
    )


def convert_deleted_user_entity_to_dto(user: entities.User) -> dto.DeletedUser:
    if not user.deleted:
        raise MappingError(f"User {user} isn't deleted")

    return dto.DeletedUser(
        id=user.id.to_uuid(),
        first_name=user.first_name,
        last_name=user.last_name,
    )
