from typing import Any, Type, TypeVar

from dataclass_factory import Retort, loader

from src.application.common.interfaces.mapper import Mapper
from src.application import user

from .user import convert_user_entity_to_dto

T = TypeVar("T")


class MapperImpl(Mapper):
    def __init__(self, retort: Retort) -> None:
        self._retort = retort

    def load(self, data: Any, class_: Type[T]) -> T:
        return self._retort.load(data, class_)


def build_mapper() -> MapperImpl:
    return MapperImpl(Retort(recipe=(
        loader(user.dto.User, convert_user_entity_to_dto),
    )))
