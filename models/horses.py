import datetime

from pydantic import (
    BaseModel,
)

from models import (
    sessions,
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


class SessionsSuccessResponse(SuccessResponse):
    session: sessions.Session
    data: sessions.ListSessionsSuccessResponse
    moda: int
