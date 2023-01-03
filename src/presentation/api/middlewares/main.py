from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .context import set_request_id_middleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(BaseHTTPMiddleware, dispatch=set_request_id_middleware)
