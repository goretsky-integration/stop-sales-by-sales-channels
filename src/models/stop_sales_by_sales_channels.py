from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from enums import ChannelStopType, SalesChannel

__all__ = ('StopSaleBySalesChannel',)


class StopSaleBySalesChannel(BaseModel):
    id: UUID
    unit_uuid: Annotated[UUID, Field(validation_alias='unitId')]
    unit_name: Annotated[str, Field(validation_alias='unitName')]
    sales_channel: Annotated[
        SalesChannel,
        Field(validation_alias='salesChannelName'),
    ]
    reason: str
    started_at_local: Annotated[
        datetime,
        Field(validation_alias='startedAtLocal'),
    ]
    ended_at_local: Annotated[
        datetime | None,
        Field(validation_alias='endedAtLocal'),
    ]
    stopped_by_user_id: Annotated[
        UUID,
        Field(validation_alias='stoppedByUserId'),
    ]
    resumed_by_user_id: Annotated[
        UUID | None,
        Field(validation_alias='resumedByUserId'),
    ]
    channel_stop_type: Annotated[
        ChannelStopType,
        Field(validation_alias='channelStopType'),
    ]
