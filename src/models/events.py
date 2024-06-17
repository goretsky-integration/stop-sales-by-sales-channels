from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from enums import SalesChannel

__all__ = (
    'EventPayload',
    'Event',
)


class EventPayload(BaseModel):
    unit_name: str
    started_at: datetime
    reason: str
    sales_channel: SalesChannel


class Event(BaseModel):
    type: str = Field(default='PIZZERIA_STOP_SALES', frozen=True)
    unit_ids: UUID
    payload: EventPayload
