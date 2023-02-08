from typing import Any, Type, TypeVar

from dataclass_factory import loader, Retort

from src import application, domain
from src.application.common.interfaces.mapper import Mapper
from src.infrastructure.db import models

from .user import (
    convert_db_model_to_user_dto,
    convert_db_model_to_user_entity,
    convert_deleted_user_entity_to_dto,
    convert_db_model_to_deleted_user_dto,
    convert_user_entity_to_db_model,
    convert_user_entity_to_dto,
)
from .converter import Converter

T = TypeVar("T")


class MapperImpl(Mapper):
    def __init__(self, retort: Retort) -> None:
        self._retort = retort

    def load(self, data: Any, class_: type[T]) -> T:
        return self._retort.load(data, class_)


def build_mapper() -> MapperImpl:
    return MapperImpl(Retort(recipe=(
        Converter(domain.user.entities.User, application.user.dto.User, convert_user_entity_to_dto),
        Converter(domain.user.entities.User, application.user.dto.DeletedUser, convert_deleted_user_entity_to_dto),
        Converter(domain.user.entities.User, models.User, convert_user_entity_to_db_model),
        Converter(models.User, domain.user.entities.User, convert_db_model_to_user_entity),
        Converter(models.User, application.user.dto.User, convert_db_model_to_user_dto),
        Converter(models.User, application.user.dto.DeletedUser, convert_db_model_to_deleted_user_dto),
    )))
