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
from models import (
    horses,
)
from misc.depends.db import get as get_db  # type: ignore

router = APIRouter(
    tags=['Get horse id'],
)
logger = logging.getLogger(__name__)


@router.get('/video/{camera_id}', response_model=horses.SessionsSuccessResponse)
async def get_horse_id(
        camera_id: int,
        start_time: datetime.datetime,
        stop_time: datetime.datetime,
        conn: asyncpg.Connection = Depends(get_db),
):
    moda = await db.get_moda(
        camera_id=camera_id,
        start_time=start_time,
        stop_time=stop_time,
        conn=conn,
    )
    result = await db.get(
        camera_id=camera_id,
        start_time=start_time,
        stop_time=stop_time,
        conn=conn,
    )
    return horses.SessionsSuccessResponse(
        # data=result,
        moda=moda,
    )
