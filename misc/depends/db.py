import logging

import asyncpg  # type: ignore
import fastapi

logger = logging.getLogger(__name__)


async def get(request: fastapi.Request) -> asyncpg.Connection:
    try:
        pool = request.app.db_pool
    except AttributeError:
        raise RuntimeError('Application state has no db pool')
    else:
        async with pool.acquire() as conn:
            yield conn
