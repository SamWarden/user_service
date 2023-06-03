from typing import Any, TypeVar

from adaptix import Retort

from src import application, domain
from src.application.common.exceptions import MappingError
from src.application.common.interfaces.mapper import Mapper
from src.infrastructure import event_bus
from src.infrastructure.db import models

from .converter import Converter
from .events import (
    convert_user_created_to_integration,
    convert_user_deleted_to_integration,
    convert_user_updated_to_integration,
)
from .user import (
    convert_db_model_to_deleted_user_dto,
    convert_db_model_to_user_dto,
    convert_db_model_to_user_entity,
    convert_deleted_user_entity_to_dto,
    convert_user_entity_to_db_model,
    convert_user_entity_to_dto,
)

T = TypeVar("T")


class MapperImpl(Mapper):
    def __init__(self, retort: Retort) -> None:
        self._retort = retort

    def load(self, data: Any, class_: type[T]) -> T:
        try:
            return self._retort.load(data, class_)
        except Exception as err:
            raise MappingError from err


def build_mapper() -> MapperImpl:
    return MapperImpl(
        Retort(
            recipe=(
                Converter(
                    domain.user.entities.User,
                    application.user.dto.User,
                    convert_user_entity_to_dto,
                ),
                Converter(
                    domain.user.entities.User,
                    application.user.dto.DeletedUser,
                    convert_deleted_user_entity_to_dto,
                ),
                Converter(
                    domain.user.entities.User,
                    models.User,
                    convert_user_entity_to_db_model,
                ),
                Converter(
                    models.User,
                    domain.user.entities.User,
                    convert_db_model_to_user_entity,
                ),
                Converter(models.User, application.user.dto.User, convert_db_model_to_user_dto),
                Converter(
                    models.User,
                    application.user.dto.DeletedUser,
                    convert_db_model_to_deleted_user_dto,
                ),
                Converter(
                    domain.user.events.UserCreated,
                    event_bus.events.UserCreated,
                    convert_user_created_to_integration,
                ),
                Converter(
                    domain.user.events.UserUpdated,
                    event_bus.events.UserUpdated,
                    convert_user_updated_to_integration,
                ),
                Converter(
                    domain.user.events.UserDeleted,
                    event_bus.events.UserDeleted,
                    convert_user_deleted_to_integration,
                ),
            )
        )
    )
