import logging
from collections.abc import Awaitable, Callable
from functools import partial

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameNotExist
from src.domain.common.exceptions import AppException
from src.domain.user.exceptions import UserIsDeleted, UsernameAlreadyExists
from src.domain.user.value_objects.full_name import WrongNameValue
from src.domain.user.value_objects.username import WrongUsernameValue
from src.presentation.api.controllers.responses import ErrorResponse
from src.presentation.api.controllers.responses.base import ErrorData
from src.presentation.api.controllers.responses.orjson import ORJSONResponse

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, error_handler(500))
    app.add_exception_handler(UserIdNotExist, error_handler(status.HTTP_404_NOT_FOUND))
    app.add_exception_handler(UsernameNotExist, error_handler(status.HTTP_404_NOT_FOUND))
    app.add_exception_handler(WrongUsernameValue, error_handler(status.HTTP_400_BAD_REQUEST))
    app.add_exception_handler(WrongNameValue, error_handler(status.HTTP_400_BAD_REQUEST))
    app.add_exception_handler(UserIdAlreadyExists, error_handler(status.HTTP_409_CONFLICT))
    app.add_exception_handler(UsernameAlreadyExists, error_handler(status.HTTP_409_CONFLICT))
    app.add_exception_handler(UserIsDeleted, error_handler(status.HTTP_409_CONFLICT))
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: int) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(request: Request, err: AppException, status_code: int) -> ORJSONResponse:
    return await handle_error(
        request=request,
        err=err,
        err_data=ErrorData(title=err.title, data=err),
        status=err.status,
        status_code=status_code,
    )


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=ErrorData(data=err)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_data: ErrorData,
    status: int,
    status_code: int,
) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=err_data, status=status),
        status_code=status_code,
    )
