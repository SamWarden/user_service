from typing import Any, Protocol, TypeVar

from adaptix import Retort

from src.application.common.exceptions import MappingError
from src.application.user import dto
from src.infrastructure.mapper.converter import Converter
from src.presentation.api.controllers import responses

from .user import convert_dto_to_users_response

T = TypeVar("T")


class Presenter(Protocol):
    def load(self, data: Any, class_: type[T]) -> T:
        raise NotImplementedError


class PresenterImpl(Presenter):
    def __init__(self, retort: Retort) -> None:
        self._retort = retort

    def load(self, data: Any, class_: type[T]) -> T:
        try:
            return self._retort.load(data, class_)
        except Exception as err:
            raise MappingError from err


def build_presenter() -> Presenter:
    return PresenterImpl(Retort(recipe=(
        Converter(dto.Users, responses.Users, convert_dto_to_users_response),
    )))
