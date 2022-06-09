"""Offer some utils to load configuration from django settings
"""
from typing import List
from django.conf import settings
from rate_limit.exceptions import CantFindBackendRedis, InvalidConfig, ConfigNotFound
from rate_limit.tools import lookup_setting
from rate_limit.load_config_interface import ConfigLoderInterface

from enum import Enum

DEFAULT_KEY_PREFIX = "RATE_LIMIT"


class TimeLimit(Enum):
    """Provide Some Time AS Sec To Avoid Mestike"""

    SEC = 1
    MIN = SEC * 60
    HOUR = MIN * 60
    DAY = HOUR * 24
    WEEKS = DAY * 7
    MONTH = DAY * 30
    YEAR = MONTH * 12


class BaseConfigLoder(ConfigLoderInterface):
    """Base Class For Creating New Config Loader,
    Providing Some Of Common Base Method For Config Loaders

    Args:
        ConfigLoderInterface (interface): Config Loader Interface
    """

    def __init__(self, settings, targets: List[str]) -> None:
        self.settings = settings
        self.targets = targets

    def find_config(self, settings, targets: list):
        """Find Configuration From Settings

        Raises:
            ConfigNotFound: Configuration not found in the settings

        Returns: Any
        """
        if redis_settings := lookup_setting(settings, targets):
            ...
        else:
            raise ConfigNotFound(f"Configuration not found in the settings")

        return redis_settings

    def extract_config(self):
        configs = self.find_config(self.settings, self.targets)
        return configs


class LoadRedisConfigFromRateLimit(BaseConfigLoder):
    def __init__(self, settings, targets: List[str] = ["RATE_LIMIT", "REDIS"]) -> None:
        super().__init__(settings, targets)

    def extract_config(self):
        """Extract redis configuration

        Returns:
            host : str
                "redis://host:6379"
            key_prefix : str
                "RATE_LIMIT"
        """
        redis_settings = super().extract_config()
        key_prefix = redis_settings.get("KEY_PREFIX", DEFAULT_KEY_PREFIX)
        if host := redis_settings.get("LOCATION", None):
            ...
        else:
            raise InvalidConfig("Can't find LOCATION key in settings configuration")

        return host, key_prefix


class LoadRedisConfigFromCaches(BaseConfigLoder):
    def __init__(self, settings, targets: List[str] = ["CACHES", "default"]) -> None:
        super().__init__(settings, targets)

    def extract_config(self):
        """extract redis configuration

        Returns:
            host : str
                "redis://host:6379"
            key_prefix : str
                "RATE_LIMIT"
        """
        redis_settings = super().extract_config()
        key_prefix = redis_settings.get("KEY_PREFIX", DEFAULT_KEY_PREFIX)
        if host := redis_settings.get("LOCATION", None):
            ...
        else:
            raise InvalidConfig("Can't find LOCATION key in settings configuration")

        # the "LOCATION" key can contain a list of hosts
        if type(host) == list or type(host) == tuple:
            host = host[0]  # select leader host to connecting

        return host, key_prefix


class LoadKeyPerfix(BaseConfigLoder):
    def __init__(
        self, settings, targets: List[str] = ["RATE_LIMIT", "KEY_PERFIX"]
    ) -> None:
        super().__init__(settings, targets)

    def extract_config(self):
        config = super().extract_config()
        if config == None:
            return DEFAULT_KEY_PREFIX
        return config


class BaseRateLimiter(BaseConfigLoder):
    def __init__(self, settings, targets: List[str]) -> None:
        BASE_SETTING: list = ["RATE_LIMIT", "RATE"]
        self.settings = settings
        self.targets = BASE_SETTING + targets

    def extract_config(self):
        user_limt_config = super().extract_config()
        max_rate, time = user_limt_config.split("/")
        return max_rate, time


class UserLimit(BaseRateLimiter):
    def __init__(self, settings, targets: List[str] = ["user"]) -> None:
        super().__init__(settings, targets)


class IPLimit(BaseRateLimiter):
    def __init__(self, settings, targets: List[str] = ["ip"]) -> None:
        super().__init__(settings, targets)


class AnonymousLimit(BaseRateLimiter):
    def __init__(self, settings, targets: List[str] = ["anonymous"]) -> None:
        super().__init__(settings, targets)


class LimitBy(BaseRateLimiter):
    def __init__(self, settings, targets: List[str]) -> None:
        super().__init__(settings, targets)
