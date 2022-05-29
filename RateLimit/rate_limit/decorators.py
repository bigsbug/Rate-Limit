from django.http import HttpRequest


def rate_limit(max_rate=1):
    def decorator(func):
        def inner(request: HttpRequest, *args, **kwargs):
            print(request.headers)
            print(f"The Decorator rate_limit is runed wiht max_rate {max_rate}")
            return func(request, *args, **kwargs)

        return inner

    return decorator
