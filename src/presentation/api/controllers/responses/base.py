from dataclasses import dataclass, field
from typing import Generic, TypeVar

TResult = TypeVar("TResult")
TError = TypeVar("TError")


@dataclass(frozen=True)
class Response:
    pass


@dataclass(frozen=True)
class OkResponse(Response, Generic[TResult]):
    status: int = 200
    result: TResult | None = None


@dataclass(frozen=True)
class ErrorData(Generic[TError]):
    title: str = "Unknown error occurred"
    data: TError | None = None


@dataclass(frozen=True)
class ErrorResponse(Response, Generic[TError]):
    status: int = 500
    error: ErrorData[TError] = field(default_factory=ErrorData)
