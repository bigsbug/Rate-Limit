from typing import Any
from django.http import HttpRequest


def get_ip(request: HttpRequest) -> str:
    headers = request.headers
    if ip := headers.get("X-Forwarded-For", None):
        ip = str.strip(ip.split(",")[0])  # X-Forwarded-For can contain multi IP
    elif ip := headers.get("X-Real-IP", None):
        ...
    else:
        return None

    return ip


def lookup_setting(settings, settings_name):
    """lookuping  the setting for attribute and sub-attribute

    Args:
        settings (class): django settings
        settings_name (list,tuple): a list of attributes

    Returns:
        dict : value of the last attribute
    """
    config = None
    if len(settings_name) > 1:
        for config_name in settings_name:
            if config is None:
                config = getattr(settings, config_name, {})
            else:
                config = config.get(str(config_name), {})
        return config
    else:
        return getattr(settings, str(settings_name[0]), {})


class Settings:
    RATE_LIMIT = {
        "REDIS": {
            "LOCATION": "redis://redis-db:6379/1",
        },
        "RATE": {
            "user": "1000/day",
            "ip": "10/min",
            "anonymous": "100/day",
        },
    }


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis-db:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "example",
    }
}
