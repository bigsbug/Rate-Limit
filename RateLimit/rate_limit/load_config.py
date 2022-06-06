from typing import List
from django.conf import settings
from exceptions import CantFindBackendRedis, InvalidConfig, ConfigNotFound
from tools import settings_have
from load_config_interface import ConfigLoderInterface

DEFAULT_KEY_PREFIX = "RATE_LIMIT"


class BaseConfigLoder(ConfigLoderInterface):
    def __init__(self, settings, targets: List[str]) -> None:
        self.settins = settings
        self.targets = targets

    def find_config(self, settings, *targets: list):
        """Find configuration from settings

        Raises:
            ConfigNotFound: Configuration not found in the settings

        Returns: Any
        """
        if redis_settings := settings_have(settings, *targets):
            ...
        else:
            raise ConfigNotFound(f"Configuration not found in the settings")

        return redis_settings

    def extract_config(self):
        configs = self.find_config(self.settins, *self.targets)
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


def show_settings():
    ...
