from typing import Any, Protocol, TypeVar

from dataclass_factory import Retort

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
        return self._retort.load(data, class_)


def build_presenter() -> Presenter:
    return PresenterImpl(Retort(recipe=(
        Converter(dto.Users, responses.Users, convert_dto_to_users_response),
    )))
