from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from uuid6 import uuid7


async def set_request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request.state.request_id = uuid7()
    response = await call_next(request)
    return response
