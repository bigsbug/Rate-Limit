from typing import Callable
from django.http import HttpRequest
from rate_limit.tools import get_ip
from rate_limit.load_config import show_settings


def rate_limit(max_rate=1):
    def decorator(func: Callable):
        def inner(request: HttpRequest, *args, **kwargs):

            ip = get_ip(request)
            show_settings()
            # print(
            #     f"The Decorator rate_limit is runed wiht max_rate {max_rate} for ip {ip}"
            # )
            return func(request, *args, **kwargs)

        return inner

    return decorator
