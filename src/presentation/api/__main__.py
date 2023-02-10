import asyncio

import structlog

from src.application.common.interfaces.mapper import Mapper
from src.infrastructure.config_loader import load_config
from src.infrastructure.di import init_di_builder, setup_di_builder
from src.infrastructure.constants import APP_SCOPE
from src.infrastructure.event_bus.event_bus import EventBusImpl
from src.infrastructure.event_bus.main import declare_exchanges
from src.infrastructure.mediator import init_mediator, setup_mediator
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
        mediator = await di_builder.execute(init_mediator, APP_SCOPE, state=di_state)
        setup_mediator(mediator)

        event_bus = await di_builder.execute(EventBusImpl, APP_SCOPE, state=di_state)
        await declare_exchanges(event_bus)

        mapper = await di_builder.execute(Mapper, APP_SCOPE, state=di_state)

        app = init_api(mediator, mapper, di_builder, di_state)
        await run_api(app, config.api)


if __name__ == "__main__":
    asyncio.run(main())
