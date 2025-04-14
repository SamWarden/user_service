from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

default_router = APIRouter(
    prefix="",
    tags=["default"],
    include_in_schema=False,
)


@default_router.get("/")
async def default_redirect() -> RedirectResponse:
    return RedirectResponse(
        "/docs",
        status_code=status.HTTP_302_FOUND,
    )
