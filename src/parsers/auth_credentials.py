from collections import defaultdict
import json

import httpx
from pydantic import TypeAdapter, ValidationError

from logger import create_logger
from models import AccountTokens, AccountUnits
from models.units import Unit

__all__ = ('parse_account_tokens_response', 'parse_units_response')

logger = create_logger('parser')


def parse_account_tokens_response(response: httpx.Response) -> AccountTokens:
    """Parse the response from the account tokens response."""
    logger.info(
        'Parsing account tokens response',
        extra={'response_body': response.text}
    )
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        logger.error(
            'Failed to parse response data as JSON',
            extra={'response_body': response.text},
        )
        raise

    try:
        return AccountTokens.model_validate(response_data)
    except ValidationError:
        logger.error(
            'Failed to validate account tokens',
            extra={'response_body': response_data},
        )
        raise


def parse_units_response(response: httpx.Response) -> list[AccountUnits]:
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        logger.error(
            'Failed to parse response data as JSON',
            extra={'response_body': response.text},
        )
        raise
    
    account_name_to_units = defaultdict(list)
    
    for unit in response_data['units']:
        account_name_to_units[unit['dodo_is_api_account_name']].append(unit)
    
    units_type_adapter = TypeAdapter(list[Unit])
    
    return [
        AccountUnits(
            account_name=account_name,
            units=units_type_adapter.validate_python(units)
        )
        for account_name, units in account_name_to_units.items()
    ]
