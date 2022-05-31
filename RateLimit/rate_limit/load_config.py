from django.conf import settings
from rate_limit.exceptions import CantFindBackendRedis, InvalidConfig
from rate_limit.tools import settings_have

DEFAULT_KEY_PREFIX = "RATE_LIMIT"


class LoadRedsiSettings:
    def __init__(self, settings) -> None:
        self.settings = settings

    def find_redis_config(self) -> dict:
        """find redis configuration from settings

        Raises:
            CantFindBackendRedis: Can't find backend redis in settings

        Returns:
            dict: {
                "LOCATOIN":"redis://host:6379",
                "KEY_PREFIX":"RATE_LIMIT"
            }
        """
        if redis_settings := settings_have(self.settings, "RATE_LIMIT", "REDIS"):
            ...
        elif redis_settings := settings_have(self.settings, "CACHES", "default"):
            if "RedisCache" not in redis_settings.get("BACKEND", ""):
                raise CantFindBackendRedis(
                    "configuration not found for Redis in settings please read the documents for more details in this [link]."
                )
        else:
            raise CantFindBackendRedis(
                "configuration not found for Redis in settings please read the documents for more details in this [link]."
            )

        return redis_settings

    def extract_config(self):
        """extract redis configuration

        Returns:
            host : str
                "redis://host:6379"
            key_prefix : str
                "RATE_LIMIT"
        """
        redis_settings = self.find_redis_config()
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
