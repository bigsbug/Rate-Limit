from django.shortcuts import render, HttpResponse
from rate_limit.decorators import rate_limit


@rate_limit(max_rate=10)
def index(request):
    return HttpResponse("you successfully access to site")
