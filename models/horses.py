import datetime

from pydantic import (
    BaseModel,
)
from models.base import (
    SuccessResponse,
)


class Horse(BaseModel):
    id: int
    horse_id: int
    horse_name: str
    camera_id: int
    even_type: str
    duration: int
    date: datetime.datetime
    start: int
    stop: int
    absolute_start: datetime.datetime
    absolute_stop: datetime.datetime


class Session(BaseModel):
    session_start_time: datetime.datetime
    id_start_time: int
    session_end_time: datetime.datetime
    id_end_time: int
    horses: list[Horse]


class SessionsSuccessResponse(SuccessResponse):
    data: list[Session]
    moda: int
