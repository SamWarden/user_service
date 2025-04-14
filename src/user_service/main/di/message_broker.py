from collections.abc import AsyncGenerator

import aio_pika
from aio_pika.pool import Pool


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
