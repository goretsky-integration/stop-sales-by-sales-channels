import asyncio
import datetime

from fast_depends import Depends, inject

from config import Config, get_config
from connections.storage import StorageConnection
from connections.dodo_is import DodoIsApiConnection
from connections.event_publisher import EventPublisher
from context.auth_credentials_storage import AuthCredentialsFetcher
from context.dodo_is import StopSalesFetcher
from dependencies import (
    get_storage_connection,
    get_dodo_is_connection,
    get_event_publisher,
)
from enums import SalesChannel
from filters import (
    filter_by_sales_channels, filter_complete_stop_sales,
    filter_not_ended_stop_sales,
)
from logger import create_logger, setup_logging
from mappers import map_stop_sales_to_events
from models import AccountUnits
from parsers.auth_credentials import parse_account_tokens_response, parse_units_response
from time_helpers import Period
from units import load_units

logger = create_logger('main')


@inject
async def main(
        storage_connection: StorageConnection = Depends(get_storage_connection),
        dodo_is_connection: DodoIsApiConnection = Depends(get_dodo_is_connection),
        config: Config = Depends(get_config),
        event_publisher: EventPublisher = Depends(get_event_publisher),
) -> None:
    setup_logging()
    
    response = await storage_connection.get_units()
    accounts_units = parse_units_response(response)

    period = Period.today_to_this_moment(timezone=config.timezone)

    auth_credentials_fetch_unit_of_work = AuthCredentialsFetcher(
        connection=storage_connection,
    )
    for account_units in accounts_units:
        auth_credentials_fetch_unit_of_work.register_account_name(
            account_name=account_units.account_name,
        )

    accounts_tokens = await auth_credentials_fetch_unit_of_work.fetch_all()
    account_name_to_access_token = {
        account_tokens.account_name: account_tokens.access_token
        for account_tokens in accounts_tokens
    }

    stop_sales_fetch_unit_of_work = StopSalesFetcher(
        connection=dodo_is_connection,
    )

    for account_units in accounts_units:
        access_token = account_name_to_access_token[account_units.account_name]
        unit_uuids = [unit.uuid for unit in account_units.units]

        stop_sales_fetch_unit_of_work.register_task(
            access_token=access_token,
            unit_uuids=unit_uuids,
        )

    stop_sales_fetch_result = await stop_sales_fetch_unit_of_work.fetch_all(
        period=Period(
            from_date=period.from_date - datetime.timedelta(days=1),
            to_date=period.to_date,
        ),
    )

    stop_sales = stop_sales_fetch_result.stop_sales

    for unit_uuid in stop_sales_fetch_result.error_unit_uuids:
        logger.error(
            'Failed to fetch stop sales',
            extra={'unit_uuid': unit_uuid},
        )

    stop_sales = filter_not_ended_stop_sales(stop_sales)
    stop_sales = filter_complete_stop_sales(stop_sales)
    stop_sales = filter_by_sales_channels(
        stop_sales=stop_sales,
        sales_channels=[SalesChannel.DINE_IN, SalesChannel.DELIVERY],
    )

    events = map_stop_sales_to_events(stop_sales)

    logger.debug('Stop sales', extra={
        'stop_sales': stop_sales,
    })

    await event_publisher.publish_all(events)


if __name__ == '__main__':
    asyncio.run(main())
