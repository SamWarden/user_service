from fastapi import FastAPI

from .healthcheck import healthcheck_router
from .user import user_router


def setup_controllers(app: FastAPI) -> None:
    app.include_router(healthcheck_router)
    app.include_router(user_router)
