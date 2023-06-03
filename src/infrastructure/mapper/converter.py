from typing import Any, Callable, Generic, TypeVar

from adaptix import Loader, Mediator, Request
from adaptix._internal.provider import LoaderProvider, LoaderRequest
from adaptix._internal.provider.request_filtering import ExactOriginRC

FromModel = TypeVar("FromModel", bound=Any)
ToModel = TypeVar("ToModel", bound=Any)
Unknown = object


class Converter(LoaderProvider, Generic[FromModel, ToModel]):
    def __init__(
        self,
        from_cls: type[FromModel],
        to_cls: type[ToModel],
        loader: Callable[[FromModel], ToModel],
    ) -> None:
        self._from_cls = from_cls
        self._to_cls = to_cls
        self._loader = loader
        self._request_checker = ExactOriginRC(to_cls)

    def _check_request(self, mediator: Mediator[ToModel], request: Request[ToModel]) -> None:
        self._request_checker.check_request(mediator, request)

    def _provide_loader(self, mediator: Mediator[ToModel], request: LoaderRequest[ToModel]) -> Loader[ToModel]:
        next_loader = mediator.provide_from_next()

        def _converter(data: Unknown) -> ToModel:
            if isinstance(data, self._from_cls):
                _loader = self._loader
            else:
                _loader = next_loader
            return _loader(data)

        return _converter
