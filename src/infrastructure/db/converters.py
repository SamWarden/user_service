from datetime import datetime
from typing import cast

from src.application.common.exceptions import MappingError
from src.application.user import dto
from src.domain.user import entities, value_objects as vo
from src.domain.user.value_objects import Username
from src.domain.user.value_objects.deleted_status import DeletionTime
from src.infrastructure.db import models


def convert_user_entity_to_db_model(user: entities.User) -> models.User:
    return models.User(
        id=user.id.to_raw(),
        username=user.username.to_raw(),
        first_name=user.full_name.first_name,
        last_name=user.full_name.last_name,
        middle_name=user.full_name.middle_name,
        deleted_at=user.deleted_at.to_raw(),
    )


def convert_db_model_to_user_entity(user: models.User, existing_usernames: set[Username]) -> entities.User:
    full_name = vo.FullName(
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
    )
    return entities.User(
        id=vo.UserId(user.id),
        username=vo.Username(user.username),
        full_name=full_name,
        deleted_at=DeletionTime(user.deleted_at),
        existing_usernames=existing_usernames,
    )


def convert_db_model_to_active_user_dto(user: models.User) -> dto.User:
    if user.deleted_at is not None:
        raise MappingError(f"User {user} is deleted")

    return dto.User(
        id=user.id,
        username=cast(str, user.username),
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
    )


def convert_db_model_to_deleted_user_dto(user: models.User) -> dto.DeletedUser:
    if user.deleted_at is None:
        raise MappingError(f"User {user} isn't deleted")

    return dto.DeletedUser(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
        deleted_at=cast(datetime, user.deleted_at),
    )


def convert_db_model_to_user_dto(user: models.User) -> dto.UserDTOs:
    match user:
        case models.User(deleted_at=None):
            return convert_db_model_to_active_user_dto(user)
        case models.User(deleted_at=True):
            return convert_db_model_to_deleted_user_dto(user)
        case _:
            raise MappingError(f"User {user} is invalid")
