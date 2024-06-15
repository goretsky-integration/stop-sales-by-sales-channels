import json

import httpx
from pydantic import TypeAdapter, ValidationError

from logger import create_logger
from models import StopSaleBySector

__all__ = ('parse_stop_sales_by_ingredients_response',)

logger = create_logger('parser')


def parse_stop_sales_by_ingredients_response(
        response: httpx.Response,
) -> list[StopSaleBySector]:
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

    type_adapter = TypeAdapter(list[StopSaleBySector])

    try:
        return type_adapter.validate_python(
            response_data['stopSalesByIngredients'],
        )
    except ValidationError:
        logger.error(
            'Failed to parse stop sales by ingredients [pydantic]',
            extra={'response_body': response.text}
        )
        raise
