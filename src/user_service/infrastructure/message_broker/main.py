from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aio_pika
from aio_pika.pool import Pool

from user_service.infrastructure.message_broker.factories import ChannelFactory, ConnectionFactory

from .config import EventBusConfig


@asynccontextmanager
async def build_rq_connection_pool(
    event_bus_config: EventBusConfig,
) -> AsyncGenerator[Pool[aio_pika.abc.AbstractConnection], None]:
    rq_connection_pool = Pool(ConnectionFactory(event_bus_config).get_connection, max_size=10)
    async with rq_connection_pool:
        yield rq_connection_pool


@asynccontextmanager
async def build_rq_channel_pool(
    rq_connection_pool: Pool[aio_pika.abc.AbstractConnection],
) -> AsyncGenerator[Pool[aio_pika.abc.AbstractChannel], None]:
    rq_channel_pool = Pool(ChannelFactory(rq_connection_pool).get_channel, max_size=100)
    async with rq_channel_pool:
        yield rq_channel_pool
