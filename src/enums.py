from enum import StrEnum, auto

__all__ = ('CountryCode', 'SalesChannel', 'ChannelStopType')


class CountryCode(StrEnum):
    RU = auto()


class SalesChannel(StrEnum):
    DINE_IN = 'Dine-in'
    TAKEAWAY = 'Takeaway'
    DELIVERY = 'Delivery'


class ChannelStopType(StrEnum):
    COMPLETE = 'Complete'
    REDIRECTION = 'Redirection'
