from typing import Callable
from django.http import HttpRequest
from rate_limit.tools import get_ip
<<<<<<< HEAD
=======
from rate_limit.load_config import show_settings
>>>>>>> 7b2fa517cc04c38737306ed35ca898f966cd4e95


def rate_limit(max_rate=1):
    def decorator(func: Callable):
        def inner(request: HttpRequest, *args, **kwargs):

            ip = get_ip(request)
<<<<<<< HEAD
            print(
                f"The Decorator rate_limit is runed wiht max_rate {max_rate} for ip {ip}"
            )
=======
            show_settings()
            # print(
            #     f"The Decorator rate_limit is runed wiht max_rate {max_rate} for ip {ip}"
            # )
>>>>>>> 7b2fa517cc04c38737306ed35ca898f966cd4e95
            return func(request, *args, **kwargs)

        return inner

    return decorator
