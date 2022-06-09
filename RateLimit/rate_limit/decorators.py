"""Decorators For Apply Some Limiting To Views"""
from typing import List, Callable
from django.http import HttpRequest, HttpResponse
from rate_limit.db_manager import (
    LoadRedisConfigFromRateLimit,
    PerformActionRedis,
    Redis,
    settings,
)
from rate_limit.limiters import BaseRateLimit

myredis = Redis()
redis_config = LoadRedisConfigFromRateLimit(settings)
myredis.load_config(redis_config)
myredis.connect()
performaction = PerformActionRedis()
performaction.set_db(myredis)


def rate_limit(type_limits: List[BaseRateLimit]):
    def _rate_limit(func: Callable):
        def inner(request: HttpRequest, *args, **kwargs):
            for type_limit in type_limits:
                type_limit.set_db(performaction)
                if type_limit.get_rate(request) >= type_limit.max_rate:
                    return HttpResponse("You cant access now to this site")
                count_rates = type_limit.new_view(request)
                request.count_hit = count_rates

                return func(request, *args, **kwargs)

        return inner

    return _rate_limit
