import logging

import uvicorn
from di import ScopeState
from didiator import Mediator
from didiator.interface.utils.di_builder import DiBuilder
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.presentation.api.controllers import setup_controllers
from src.presentation.api.middlewares import setup_middlewares
from src.presentation.api.providers import setup_providers

from .config import APIConfig

logger = logging.getLogger(__name__)


def init_api(
    mediator: Mediator,
    di_builder: DiBuilder,
    di_state: ScopeState | None = None,
    debug: bool = __debug__,
) -> FastAPI:
    logger.debug("Initialize API")
    app = FastAPI(
        debug=debug,
        title="User service",
        version="1.0.0",
        default_response_class=ORJSONResponse,
    )
    setup_providers(app, mediator, di_builder, di_state)
    setup_middlewares(app)
    setup_controllers(app)
    return app


async def run_api(app: FastAPI, api_config: APIConfig) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
        log_level=logging.INFO,
        log_config=None,
    )
    server = uvicorn.Server(config)
    logger.info("Running API")
    await server.serve()
