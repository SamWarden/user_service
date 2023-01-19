from dataclass_factory.load_error import ValueLoadError

from src.application.user import dto
from src.domain.user import entities, value_objects as vo
from src.infrastructure.db import models


def convert_user_entity_to_dto(user: entities.User) -> dto.User:
    if not isinstance(user, entities.User):
        raise ValueLoadError(f"Wrong mapping type: {type(user)}")
    if user.deleted:
        raise ValueLoadError(f"User {user} is deleted")

    return dto.User(
        id=user.id.to_uuid(),
        username=str(user.username),
        first_name=user.first_name,
        last_name=user.last_name,
    )


def convert_deleted_user_entity_to_dto(user: entities.User) -> dto.DeletedUser:
    if not isinstance(user, entities.User):
        raise ValueLoadError(f"Wrong mapping type: {type(user)}")
    if not user.deleted:
        raise ValueLoadError(f"User {user} isn't deleted")

    return dto.DeletedUser(
        id=user.id.to_uuid(),
        first_name=user.first_name,
        last_name=user.last_name,
    )


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    if not isinstance(user, entities.User):
        raise ValueLoadError(f"Wrong mapping type: {type(user)}")

    return models.User(
        id=user.id.to_uuid(),
        username=str(user.username),
        first_name=user.first_name,
        last_name=user.last_name,
        deleted=user.deleted,
    )


def convert_db_model_to_user_entity(user: models.User) -> entities.User:
    if not isinstance(user, models.User):
        raise ValueLoadError(f"Wrong mapping type: {type(user)}")

    return entities.User(
        id=user.id,
        username=vo.Username(user.username),
        first_name=user.first_name,
        last_name=user.last_name,
        deleted=user.deleted,
    )


def convert_db_model_to_user_dto(user: models.User) -> dto.User:
    if not isinstance(user, models.User):
        raise ValueLoadError(f"Wrong mapping type: {type(user)}")
    if user.deleted:
        raise ValueLoadError(f"User {user} is deleted")

    return dto.User(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )


def convert_deleted_user_model_to_dto(user: models.User) -> dto.DeletedUser:
    if not isinstance(user, models.User):
        raise ValueLoadError(f"Wrong mapping type: {type(user)}")
    if not user.deleted:
        raise ValueLoadError(f"User {user} isn't deleted")

    return dto.DeletedUser(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
    )
