import datetime
import logging

import asyncpg  # type: ignore
from fastapi import (
    APIRouter,
    Depends,
)

from misc import (
    db,
)
from misc.depends.db import get as get_db  # type: ignore
from misc.handlers import (
    error_404,
)
from models import (
    horses as model_horse,
    sessions as model_session,
)

router = APIRouter(
    tags=['Get horse id'],
)
logger = logging.getLogger(__name__)


@router.get('/video/{camera_id}', response_model=model_horse.SessionsSuccessResponse)
async def get_horse_id(
        camera_id: int,
        start_time: datetime.datetime,
        stop_time: datetime.datetime,
        conn: asyncpg.Connection = Depends(get_db),
):
    session = await db.get_session(
        camera_id=camera_id,
        start_time=start_time,
        stop_time=stop_time,
        conn=conn,
    )
    if not session:
        return await error_404('Session not found')
    actions = await db.get_session_actions(
        id_start=session.horses_id_start_session,
        id_end=session.horses_id_end_session,
        conn=conn,
    )
    total = await db.get_sessions_count(
        conn=conn,
    )
    return model_horse.SessionsSuccessResponse(
        session=session,
        data=model_session.ListSessionsSuccessResponse(
            total=total,
            items=actions

        ),
        moda=actions.data[0].horse_id,  # type: ignore
    )
