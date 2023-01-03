import asyncio
import os

from didiator import Mediator
from src.infrastructure.di import setup_di_builder, setup_mediator_factory
from src.infrastructure.constants import APP_SCOPE, REQUEST_SCOPE
from src.infrastructure.factories.mediator import create_mediator_builder
from src.presentation.api.main import init_api, run_api

CONFIG_PATH: str = os.getenv("CONFIG_PATH", "./config.toml")


async def main() -> None:
    # config = load_config(CONFIG_PATH)

    di_builder = setup_di_builder()

    async with di_builder.enter_scope(APP_SCOPE) as di_state:
        mediator = await di_builder.execute(Mediator, APP_SCOPE, state=di_state)
        setup_mediator_factory(di_builder, create_mediator_builder(mediator), REQUEST_SCOPE)

        app = init_api(mediator, di_builder, di_state)
        await run_api(app)


if __name__ == "__main__":
    asyncio.run(main())
