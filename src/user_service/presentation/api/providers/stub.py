import inspect
from collections.abc import Callable, Hashable
from typing import Annotated, Any, Never, ParamSpec, TypeVar

from fastapi import Depends


class Stub:
    def __init__(self, dependency: Callable, **kwargs: Hashable) -> None:
        self._dependency = dependency
        self._kwargs = kwargs

    def __call__(self) -> Never:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Stub):
            return self._dependency == other._dependency and self._kwargs == other._kwargs
        if not self._kwargs:
            return self._dependency == other
        return False

    def __hash__(self) -> int:
        if not self._kwargs:
            return hash(self._dependency)
        serial = (
            self._dependency,
            *self._kwargs.items(),
        )
        return hash(serial)


P = ParamSpec("P")
T = TypeVar("T")


def wrap_factory(factory: Callable[P, T], **kwargs: Callable[..., Any]) -> Callable[P, T]:
    def provider(*args: P.args, **kwargs: P.kwargs) -> T:
        return factory(*args, **kwargs)

    factory_sig = inspect.signature(factory)
    new_params: list[inspect.Parameter] = []
    for param in factory_sig.parameters.values():
        if param.name in kwargs:
            stub = kwargs[param.annotation]
        else:
            stub = Stub(param.annotation)
        new_params.append(param.replace(annotation=Annotated[param.annotation, Depends(stub)]))

    provider_sig = inspect.signature(provider)
    new_sig = provider_sig.replace(parameters=new_params, return_annotation=factory_sig.return_annotation)
    new_hints = {param.name: param.annotation for param in new_params}
    provider.__signature__ = new_sig  # type: ignore[attr-defined]
    provider.__annotations__ = new_hints
    return provider
