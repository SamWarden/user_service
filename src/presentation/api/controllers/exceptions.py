import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request

from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameAlreadyExists, UsernameNotExist
from src.domain.common.exceptions import AppException
from src.domain.user.exceptions import UserIsDeleted
from src.domain.user.value_objects.full_name import WrongNameValue
from src.domain.user.value_objects.username import WrongUsernameValue
from src.presentation.api.controllers.responses import ErrorResult

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserIdNotExist, user_id_not_exist_handler)
    app.add_exception_handler(UsernameNotExist, username_not_exist_handler)
    app.add_exception_handler(WrongUsernameValue, wrong_username_value_handler)
    app.add_exception_handler(WrongNameValue, wrong_name_value_handler)
    app.add_exception_handler(UserIdAlreadyExists, user_id_already_exists_handler)
    app.add_exception_handler(UsernameAlreadyExists, username_already_exists_handler)
    app.add_exception_handler(UserIsDeleted, user_is_deleted_handler)
    app.add_exception_handler(Exception, unknown_exception_handler)


async def user_id_not_exist_handler(request: Request, err: UserIdNotExist) -> ORJSONResponse:
    return await handle_error(request, err, status_code=status.HTTP_404_NOT_FOUND)


async def username_not_exist_handler(request: Request, err: UsernameNotExist) -> ORJSONResponse:
    return await handle_error(request, err, status_code=status.HTTP_404_NOT_FOUND)


async def wrong_username_value_handler(request: Request, err: WrongUsernameValue) -> ORJSONResponse:
    return await handle_error(request, err, status_code=status.HTTP_400_BAD_REQUEST)


async def wrong_name_value_handler(request: Request, err: WrongNameValue) -> ORJSONResponse:
    return await handle_error(request, err, status_code=status.HTTP_400_BAD_REQUEST)


async def user_id_already_exists_handler(request: Request, err: UserIdAlreadyExists) -> ORJSONResponse:
    return await handle_error(request, err, status_code=status.HTTP_409_CONFLICT)


async def username_already_exists_handler(request: Request, err: UsernameAlreadyExists) -> ORJSONResponse:
    return await handle_error(request, err, status_code=status.HTTP_409_CONFLICT)


async def user_is_deleted_handler(request: Request, err: UserIsDeleted) -> ORJSONResponse:
    return await handle_error(request, err, status_code=status.HTTP_409_CONFLICT)


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResult(message="Unknown server error has occurred", data=err),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(request: Request, err: AppException, status_code: int) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResult(message=err.message, data=err),
        status_code=status_code,
    )
