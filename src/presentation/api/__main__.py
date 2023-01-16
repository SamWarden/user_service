import asyncio

import structlog
from didiator import Mediator
from src.infrastructure.di import setup_di_builder, setup_mediator_factory
from src.infrastructure.constants import APP_SCOPE, CONFIG_PATH, REQUEST_SCOPE
from src.infrastructure.factories.mediator import create_mediator_builder
from src.infrastructure.log import configure_logging
from src.presentation.api.config import load_config
from src.presentation.api.main import init_api, run_api

logger = structlog.get_logger()


async def main() -> None:
    config = load_config(CONFIG_PATH)
    configure_logging(config.logging)

    logger.info("Launch app")

    di_builder = setup_di_builder()

    async with di_builder.enter_scope(APP_SCOPE) as di_state:
        mediator = await di_builder.execute(Mediator, APP_SCOPE, state=di_state)
        setup_mediator_factory(di_builder, create_mediator_builder(mediator), REQUEST_SCOPE)

        app = init_api(mediator, di_builder, di_state)
        await run_api(app)


if __name__ == "__main__":
    asyncio.run(main())
