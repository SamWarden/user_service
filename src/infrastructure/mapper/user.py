from typing import cast

from dataclass_factory.load_error import ValueLoadError

from src.application.user import dto
from src.domain.user import entities, value_objects as vo
from src.infrastructure.db import models


def convert_user_entity_to_dto(user: entities.User) -> dto.User:
    if user.deleted:
        raise ValueLoadError(f"User {user} is deleted")

    return dto.User(
        id=user.id.to_uuid(),
        username=str(user.username),
        first_name=user.first_name,
        last_name=user.last_name,
    )


def convert_deleted_user_entity_to_dto(user: entities.User) -> dto.DeletedUser:
    if not user.deleted:
        raise ValueLoadError(f"User {user} isn't deleted")

    return dto.DeletedUser(
        id=user.id.to_uuid(),
        first_name=user.first_name,
        last_name=user.last_name,
    )


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    return models.User(
        id=user.id.to_uuid(),
        username=str(user.username) if user.username is not None else None,
        first_name=user.first_name,
        last_name=user.last_name,
        deleted=user.deleted,
    )


def convert_db_model_to_user_entity(user: models.User) -> entities.User:
    return entities.User(
        id=vo.UserId(user.id),
        username=vo.Username(user.username) if user.username is not None else None,
        first_name=user.first_name,
        last_name=user.last_name,
        deleted=user.deleted,
    )


def convert_db_model_to_user_dto(user: models.User) -> dto.User:
    if user.deleted:
        raise ValueLoadError(f"User {user} is deleted")

    return dto.User(
        id=user.id,
        username=cast(user.username, str),
        first_name=user.first_name,
        last_name=user.last_name,
    )


def convert_db_model_to_deleted_user_dto(user: models.User) -> dto.DeletedUser:
    if not user.deleted:
        raise ValueLoadError(f"User {user} isn't deleted")

    return dto.DeletedUser(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
    )
