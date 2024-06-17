import json

import httpx
from pydantic import TypeAdapter, ValidationError

from logger import create_logger
from models import StopSaleBySalesChannel

__all__ = ('parse_stop_sales_by_sales_channels_response',)

logger = create_logger('parser')


def parse_stop_sales_by_sales_channels_response(
        response: httpx.Response,
) -> list[StopSaleBySalesChannel]:
    logger.info(
        'Parsing account tokens response',
        extra={'response_body': response.text}
    )
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        logger.error(
            'Failed to parse response JSON',
            extra={'response_body': response.text}
        )
        raise

    type_adapter = TypeAdapter(list[StopSaleBySalesChannel])

    try:
        return type_adapter.validate_python(
            response_data['stopSalesBySalesChannels'],
        )
    except ValidationError:
        logger.error(
            'Failed to parse stop sales by sales channels [pydantic]',
            extra={'response_body': response.text}
        )
        raise
