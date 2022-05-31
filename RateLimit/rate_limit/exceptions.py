class CantFindBackendRedis(Exception):
    """Cant Find Backend Redis in default CACHE settings"""


class InvalidHostOrPort(Exception):
    """The hsot or port is invalid"""


class InvalidConfig(Exception):
    """The Config is invalid"""
