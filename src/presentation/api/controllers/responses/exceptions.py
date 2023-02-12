from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic.generics import GenericModel

TData = TypeVar("TData")


@dataclass(frozen=True)
class ErrorResult(GenericModel, Generic[TData]):
    message: str
    data: TData
