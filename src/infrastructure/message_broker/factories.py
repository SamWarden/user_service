import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from .config import EventBusConfig


class ConnectionFactory:
    def __init__(self, config: EventBusConfig) -> None:
        self._config = config

    async def get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(
            host=self._config.host,
            port=self._config.port,
            login=self._config.login,
            password=self._config.password,
        )


class ChannelFactory:
    def __init__(self, rq_connection_pool: Pool[aio_pika.abc.AbstractConnection]) -> None:
        self._rq_connection_pool = rq_connection_pool

    async def get_channel(self) -> aio_pika.abc.AbstractChannel:
        async with self._rq_connection_pool.acquire() as connection:
            return await connection.channel(publisher_confirms=False)
