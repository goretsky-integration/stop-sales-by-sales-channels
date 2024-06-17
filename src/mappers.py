from collections.abc import Iterable

from models import (
    AccountUnits,
    Event,
    EventPayload,
    StopSaleBySalesChannel,
    Unit,
)

__all__ = (
    'map_stop_sales_to_events',
    'map_accounts_units_to_units',
)


def map_stop_sales_to_events(
        stop_sales: Iterable[StopSaleBySalesChannel],
) -> list[Event]:
    events: list[Event] = []
    for stop_sale in stop_sales:
        event_payload = EventPayload(
            unit_name=stop_sale.unit_name,
            started_at=stop_sale.started_at_local,
            reason=stop_sale.reason,
            sales_channel=stop_sale.sales_channel,
        )
        event = Event(unit_ids=stop_sale.unit_uuid, payload=event_payload)
        events.append(event)

    return events


def map_accounts_units_to_units(
        accounts_units: Iterable[AccountUnits],
) -> list[Unit]:
    return [
        unit
        for account_units in accounts_units
        for unit in account_units.units
    ]
