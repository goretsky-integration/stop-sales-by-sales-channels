from typing import NewType

import httpx

__all__ = (
    'StorageHttpClient',
    'DodoISHttpClient',
)

StorageHttpClient = NewType('StorageHttpClient', httpx.AsyncClient)
DodoISHttpClient = NewType('DodoISHttpClient', httpx.AsyncClient)
