from typing import Any, Type, TypeVar

from dataclass_factory import loader, Retort

from src import application, domain
from src.application.common.interfaces.mapper import Mapper
from src.infrastructure.db import models

from .user import (
    convert_db_model_to_user_dto,
    convert_db_model_to_user_entity,
    convert_deleted_user_entity_to_dto,
    convert_deleted_user_model_to_dto,
    convert_user_entity_to_db_model,
    convert_user_entity_to_dto,
)

T = TypeVar("T")


class MapperImpl(Mapper):
    def __init__(self, retort: Retort) -> None:
        self._retort = retort

    def load(self, data: Any, class_: Type[T]) -> T:
        return self._retort.load(data, class_)


def build_mapper() -> MapperImpl:
    return MapperImpl(Retort(recipe=(
        loader(application.user.dto.User, convert_user_entity_to_dto),
        loader(application.user.dto.DeletedUser, convert_deleted_user_entity_to_dto),
        loader(models.User, convert_user_entity_to_db_model),
        loader(application.user.dto.User, convert_db_model_to_user_dto),
        loader(application.user.dto.DeletedUser, convert_deleted_user_model_to_dto),
        loader(domain.user.entities.User, convert_db_model_to_user_entity),
    )))
