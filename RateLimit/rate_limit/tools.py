from django.http import HttpRequest


def get_ip(request: HttpRequest) -> str:
    headers = request.headers

    if ip := headers.get("X-Forwarded-For", None):
        ip = str.strip(ip.split(",")[0])  # X-Forwarded-For can contain multi IP
    elif ip := headers.get("X-Real-IP", None):
        ...
    else:
        return ""

    return ip
