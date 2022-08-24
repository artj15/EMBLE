import datetime
import logging
from typing import (
    Optional,
    List,
    Type,
    Any,
)

import asyncpg  # type: ignore
from pydantic import (
    BaseModel,
)

from models import (
    sessions,
)

logger = logging.getLogger(__name__)
HORSES = 'horses'
SESSIONS = 'sessions'


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


def record_to_model(model_cls: Type[BaseModel], record: Optional[asyncpg.Record]) -> Any:
    return model_cls.parse_obj(record) if record else None


def record_to_model_list(model_cls: Type[BaseModel], records: List[asyncpg.Record]) -> list[Any]:
    return [record_to_model(model_cls, i) for i in records] if records else []


async def get_session(
        camera_id: int,
        start_time: datetime.datetime,
        stop_time: datetime.datetime,
        conn: asyncpg.Connection,
) -> Optional[sessions.Session]:
    values = [camera_id, start_time, stop_time]
    query = f'SELECT * FROM {SESSIONS} WHERE camera_id = $1 and absolute_start >= $2 and absolute_end >= $3'
    result = await conn.fetchrow(query, *values)
    return record_to_model(sessions.Session, result)


async def get_sessions_count(
        conn: asyncpg.Connection,
) -> int:
    query = f'SELECT COUNT(*) FROM {SESSIONS}'
    result = await conn.fetchrow(query)
    return result['count']


async def get_session_actions(
        id_start: int,
        id_end: int,
        conn: asyncpg.Connection,
) -> Optional[sessions.SessionResponse]:
    values = [id_start, id_end]
    query_actions = f'''SELECT horse_id, count(*) as total_actions FROM {HORSES} where id >= $1 and id <= $2
                GROUP BY horse_id ORDER BY count(*) DESC'''
    total_actions = f'SELECT COUNT(*) FROM {HORSES} where id >= $1 and id <= $2'
    result = await conn.fetch(query_actions, *values)
    result_total = await conn.fetchrow(total_actions, *values)
    return sessions.SessionResponse(
        total_actions=result_total['count'],
        data=[sessions.HorseActions.parse_obj(model) for model in result],
    ) if result and result_total else None
