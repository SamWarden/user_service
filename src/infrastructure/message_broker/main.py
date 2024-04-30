from collections.abc import AsyncGenerator

import aio_pika
from aio_pika.pool import Pool

from src.infrastructure.message_broker.factories import ChannelFactory, ConnectionFactory

from .config import EventBusConfig


async def build_rq_connection_pool(
    event_bus_config: EventBusConfig,
) -> AsyncGenerator[Pool[aio_pika.abc.AbstractConnection], None]:
    rq_connection_pool = Pool(ConnectionFactory(event_bus_config).get_connection, max_size=10)
    async with rq_connection_pool:
        yield rq_connection_pool


async def build_rq_channel_pool(
    rq_connection_pool: Pool[aio_pika.abc.AbstractConnection],
) -> AsyncGenerator[Pool[aio_pika.abc.AbstractChannel], None]:
    rq_channel_pool = Pool(ChannelFactory(rq_connection_pool).get_channel, max_size=100)
    async with rq_channel_pool:
        yield rq_channel_pool


async def build_rq_channel(
    rq_channel_pool: Pool[aio_pika.abc.AbstractChannel],
) -> AsyncGenerator[aio_pika.abc.AbstractChannel, None]:
    async with rq_channel_pool.acquire() as channel:
        yield channel
        channel.transaction()


async def build_rq_transaction(
    rq_channel: aio_pika.abc.AbstractChannel,
) -> aio_pika.abc.AbstractTransaction:
    rq_transaction = rq_channel.transaction()
    await rq_transaction.select()
    return rq_transaction
