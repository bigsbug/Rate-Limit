from django.http import HttpRequest, HttpResponse
from rate_limit.decorators import rate_limit
from rate_limit.limiters import RateLimitAnonymous, RateLimitUser, RateLimitIP

from rate_limit.db_manager import (
    LoadRedisConfigFromRateLimit,
    PerformActionRedis,
    Redis,
    settings,
)

myredis = Redis()
redis_config = LoadRedisConfigFromRateLimit(settings)
myredis.load_config(redis_config)
myredis.connect()
performaction = PerformActionRedis()
performaction.set_db(myredis)


@rate_limit([RateLimitAnonymous()])
def index(request: HttpRequest):
    count = request.count_hit

    return HttpResponse(f"user successfully access to site {count} times")
