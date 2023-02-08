from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameAlreadyExists, UsernameNotExist
from src.application.user.validators.username import EmptyUsername, TooLongUsername, WrongUsernameFormat
from src.domain.user.exceptions import UserIsDeleted


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, exception_handler)


async def exception_handler(request: Request, err: Exception) -> JSONResponse:
    match err:
        case TooLongUsername() | EmptyUsername() | WrongUsernameFormat():
            return JSONResponse(status.HTTP_400_BAD_REQUEST)
        case UserIdNotExist() | UsernameNotExist():
            return JSONResponse(status.HTTP_404_NOT_FOUND)
        case UsernameAlreadyExists() | UserIdAlreadyExists() | UserIsDeleted():
            return JSONResponse(status.HTTP_409_CONFLICT)
        case _:
            return JSONResponse(status.HTTP_500_INTERNAL_SERVER_ERROR)
