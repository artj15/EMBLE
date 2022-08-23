import datetime
import logging
from typing import (
    Optional,
    List,
    Type,
    Union,
)

import asyncpg  # type: ignore
from pydantic import (
    BaseModel,
)

from models import (
    horses,
)

logger = logging.getLogger(__name__)


async def init(config: dict) -> asyncpg.Pool:
    dsn = config.get('dsn')
    if not dsn:
        raise RuntimeError('DB connection parameters not defined')
    return await asyncpg.create_pool(
        dsn=dsn,
    )


async def get_conn(config: dict) -> asyncpg.Connection:
    dsn = config.pop('dsn')
    if not dsn:
        raise RuntimeError('DB connection parameters not defined')
    return await asyncpg.connect(dsn, **config)


def record_to_model(model_cls: Type[BaseModel], record: Optional[asyncpg.Record]) -> Union[None, BaseModel]:
    return model_cls.parse_obj(record) if record else None


def record_to_model_list(model_cls: Type[BaseModel], records: List[asyncpg.Record]) -> list[Optional[BaseModel]]:
    return [record_to_model(model_cls, i) for i in records] if records else []


async def get_moda(
        camera_id: int,
        start_time: datetime.datetime,
        stop_time: datetime.datetime,
        conn: asyncpg.Connection,
) -> int:
    table = 'horses'
    values = [camera_id, start_time, stop_time]
    query = f'''SELECT horse_id FROM {table} WHERE camera_id = $1 and absolute_start >= $2 AND absolute_start <= $3 
                GROUP BY horse_id ORDER BY COUNT(horse_id) DESC LIMIT 1'''
    result = await conn.fetchrow(query, *values)
    return result['horse_id']


async def get(
        camera_id: int,
        start_time: datetime.datetime,
        stop_time: datetime.datetime,
        conn: asyncpg.Connection,
) -> list[Optional[BaseModel]]:
    table = 'horses'
    values = [camera_id, start_time, stop_time]
    query = f'''SELECT * FROM {table} 
                WHERE camera_id = $1 and absolute_start >= $2 AND absolute_start <= $3 
                order by horse_id'''
    result = await conn.fetch(query, *values)
    logger.info(f'{result=}')
    for session in result:
        horses.Session(
            type=res['even_type']
    return [horses.Session(
        type=res['even_type'],
    ) for res in result] if result else []
