from django.http import HttpRequest, HttpResponse
from rate_limit.decorators import rate_limit
from rate_limit.limiters import RateLimitAnonymous, RateLimitUser, RateLimitIP


@rate_limit([RateLimitAnonymous()])
def index(request: HttpRequest):
    count = request.count_hit

    return HttpResponse(f"user successfully access to site {count} times")
