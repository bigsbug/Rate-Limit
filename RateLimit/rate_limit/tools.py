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


def settings_have(
    settings, first_atter: str, second_atter: str = None, default: Any = None
):
    if second_atter:
        DATA = getattr(settings, first_atter, {}).get(str(second_atter), default)
        return DATA
    return getattr(settings, str(first_atter), default)
