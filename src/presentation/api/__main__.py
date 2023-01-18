import asyncio

import structlog
from didiator import Mediator

from src.infrastructure.config_loader import load_config
from src.infrastructure.di import init_di_builder, setup_di_builder, setup_mediator_factory
from src.infrastructure.constants import APP_SCOPE, REQUEST_SCOPE
from src.infrastructure.factories.mediator import create_mediator_builder
from src.infrastructure.log import configure_logging
from src.presentation.api.main import init_api, run_api

from .config import Config, setup_di_builder_config

logger = structlog.get_logger()


async def main() -> None:
    config = load_config(Config)
    configure_logging(config.logging)

    logger.info("Launch app")

    di_builder = init_di_builder()
    setup_di_builder(di_builder)
    setup_di_builder_config(di_builder, config)

    async with di_builder.enter_scope(APP_SCOPE) as di_state:
        mediator = await di_builder.execute(Mediator, APP_SCOPE, state=di_state)
        setup_mediator_factory(di_builder, create_mediator_builder(mediator), REQUEST_SCOPE)

        app = init_api(mediator, di_builder, di_state)
        await run_api(app, config.api)


if __name__ == "__main__":
    asyncio.run(main())
