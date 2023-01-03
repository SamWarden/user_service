import uvicorn
from di.container import ContainerState
from didiator import Mediator
from didiator.utils.di_builder import DiBuilder
from fastapi import FastAPI

from src.presentation.api.controllers.main import setup_controllers
from src.presentation.api.middlewares.main import setup_middlewares
from src.presentation.api.providers.main import setup_providers


def init_api(
    mediator: Mediator,
    di_builder: DiBuilder,
    di_state: ContainerState | None = None,
) -> FastAPI:
    app = FastAPI()
    setup_providers(app, mediator, di_builder, di_state)
    setup_middlewares(app)
    setup_controllers(app)
    return app


async def run_api(app: FastAPI) -> None:
    config = uvicorn.Config(app, port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
