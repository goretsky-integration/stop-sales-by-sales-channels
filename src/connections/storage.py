import httpx

from logger import create_logger
from new_types import StorageHttpClient

__all__ = ('StorageConnection',)

logger = create_logger('storage_connection')


class StorageConnection:

    def __init__(
            self,
            http_client: StorageHttpClient,
    ):
        self.__http_client = http_client
    
    async def get_units(self) -> httpx.Response:
        url = '/units/'
        response = await self.__http_client.get(url)
        return response

    async def get_tokens(self, account_name: str) -> httpx.Response:
        url = '/auth/token/'
        request_query_params = {'account_name': account_name}

        logger.debug(
            'Retrieving tokens for account',
            extra={'account_name': account_name},
        )
        response = await self.__http_client.get(
            url=url,
            params=request_query_params,
        )
        logger.debug(
            'Retrieved tokens for account',
            extra={
                'account_name': account_name,
                'status_code': response.status_code,
            },
        )

        return response
