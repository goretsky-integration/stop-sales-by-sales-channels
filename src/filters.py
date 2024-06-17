from collections.abc import Iterable

from enums import ChannelStopType, SalesChannel
from models import StopSaleBySalesChannel

__all__ = (
    'filter_not_ended_stop_sales',
    'filter_by_sales_channels',
    'filter_complete_stop_sales',
)


def filter_not_ended_stop_sales(
        stop_sales: Iterable[StopSaleBySalesChannel],
) -> list[StopSaleBySalesChannel]:
    return [
        stop_sale for stop_sale in stop_sales
        if stop_sale.ended_at_local is None
    ]


def filter_by_sales_channels(
        stop_sales: Iterable[StopSaleBySalesChannel],
        sales_channels: Iterable[SalesChannel],
) -> list[StopSaleBySalesChannel]:
    sales_channels = set(sales_channels)
    return [
        stop_sale for stop_sale in stop_sales
        if stop_sale.sales_channel in sales_channels
    ]


def filter_complete_stop_sales(
        stop_sales: Iterable[StopSaleBySalesChannel],
) -> list[StopSaleBySalesChannel]:
    return [
        stop_sale for stop_sale in stop_sales
        if stop_sale.channel_stop_type == ChannelStopType.COMPLETE
    ]
