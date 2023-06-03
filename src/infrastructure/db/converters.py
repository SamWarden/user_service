from typing import cast

from src.application.common.exceptions import MappingError
from src.application.user import dto
from src.domain.user import entities, value_objects as vo
from src.infrastructure.db import models


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


def convert_db_model_to_active_user_dto(user: models.User) -> dto.User:
    if user.deleted:
        raise MappingError(f"User {user} is deleted")

    return dto.User(
        id=user.id,
        username=cast(str, user.username),
        first_name=user.first_name,
        last_name=user.last_name,
    )


def convert_db_model_to_deleted_user_dto(user: models.User) -> dto.DeletedUser:
    if not user.deleted:
        raise MappingError(f"User {user} isn't deleted")

    return dto.DeletedUser(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
    )


def convert_db_model_to_user_dto(user: models.User) -> dto.UserDTOs:
    match user:
        case models.User(deleted=False):
            return convert_db_model_to_active_user_dto(user)
        case models.User(deleted=True):
            return convert_db_model_to_deleted_user_dto(user)
        case _:
            raise MappingError(f"User {user} is invalid")
