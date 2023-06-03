import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request

from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameAlreadyExists, UsernameNotExist
from src.domain.user.exceptions import UserIsDeleted
from src.domain.user.value_objects.username import EmptyUsername, TooLongUsername, WrongUsernameFormat
from src.presentation.api.controllers.responses import ErrorResult

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, exception_handler)


async def exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})

    match err:
        case TooLongUsername() | EmptyUsername() | WrongUsernameFormat() as err:
            return ORJSONResponse(
                ErrorResult(message=err.message, data=err),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case UserIdNotExist() | UsernameNotExist() as err:
            return ORJSONResponse(
                ErrorResult(message=err.message, data=err),
                status_code=status.HTTP_404_NOT_FOUND,
            )
        case UsernameAlreadyExists() | UserIdAlreadyExists() | UserIsDeleted() as err:
            return ORJSONResponse(
                ErrorResult(message=err.message, data=err),
                status_code=status.HTTP_409_CONFLICT,
            )
        case _:
            logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
            return ORJSONResponse(
                ErrorResult(message="Unknown server error has occurred", data=err),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
