import datetime

from pydantic import (
    BaseModel,
)

from models.base import (
    ListData,
)


class Session(BaseModel):
    id: int
    camera_id: int
    horses_id_start_session: int
    absolute_start: datetime.datetime
    horses_id_end_session: int
    absolute_end: datetime.datetime


class HorseActions(BaseModel):
    horse_id: int
    total_actions: int


class SessionResponse(BaseModel):
    total_actions: int
    data: list[HorseActions]


class ListSessionsSuccessResponse(ListData):
    items: SessionResponse
