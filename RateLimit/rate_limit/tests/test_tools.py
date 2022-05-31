from django.test import TestCase, RequestFactory
from rate_limit.tools import get_ip, settings_have


class ValidSettings:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379",
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            "KEY_PREFIX": "example",
        }
    }
    RATE_LIMIT = {
        "REDIS": {
            "LOCATION": "redis://127.0.0.1:6379",
            "KEY_PREFIX": "example",
        }
    }


class SettingsHaveTestCase(TestCase):
    def setUp(self) -> None:
        self.settings = ValidSettings()

    def test_settings_have_one_parameter(self):
        result = settings_have(self.settings, "RATE_LIMIT")
        excepted = self.settings.RATE_LIMIT
        self.assertEqual(result, excepted)

    def test_settings_have_second_parameter(self):
        result = settings_have(self.settings, "RATE_LIMIT", "REDIS")
        excepted = self.settings.RATE_LIMIT.get("REDIS")
        self.assertEqual(result, excepted)

    def test_settins_have_worng_parameter(self):
        result = settings_have(self.settings, "RATE_LIMIT", "RED")
        excepted = None
        self.assertEqual(result, excepted)

    def test_settins_have_worng_parameter_2(self):
        result = settings_have(self.settings, "RATE_LIMITS", "REDIS")
        excepted = None
        self.assertEqual(result, excepted)


class GetIpTestCase(TestCase):
    def setUp(self) -> None:
        self.requestr = RequestFactory()

        # Request With Header X-Real-IP
        self.valid_headers_X_Real_IP = {
            "HTTP_X-Real-IP": "127.0.0.1",
        }
        self.reqeust_with_X_Real_Ip = self.requestr.get(
            "some-path", **self.valid_headers_X_Real_IP
        )

        # Request With Header X-Forwarded-For
        self.valid_headers_X_Forwarded_For = {
            "HTTP_X-Forwarded-For": "127.0.0.1",
        }
        self.reqeust_with_X_Forwarded_For = self.requestr.get(
            "some-path", **self.valid_headers_X_Forwarded_For
        )

        # Request With Header X-Forwarded-For With Multi IP
        self.valid_headers_X_Forwarded_For_With_Multi_Ip = {
            "HTTP_X-Forwarded-For": "127.0.0.1, 127.0.0.2, 198.165.173.123, 0.0.0.0",
        }
        self.reqeust_with_X_Forwarded_For_With_Multi_IP = self.requestr.get(
            "some-path", **self.valid_headers_X_Forwarded_For_With_Multi_Ip
        )

        # Request Without Valid Headers
        self.invalid_headers = {}
        self.reqeust_with_Invalid_Headers = self.requestr.get(
            "some-path", **self.invalid_headers
        )

    def test_get_ip_X_Real_IP(self):
        result = get_ip(self.reqeust_with_X_Real_Ip)
        excepted = "127.0.0.1"
        self.assertEqual(result, excepted)

    def test_get_ip_X_Forwarded_For(self):
        result = get_ip(self.reqeust_with_X_Forwarded_For)
        excepted = "127.0.0.1"
        self.assertEqual(result, excepted)

    def test_get_ip_X_Forwarded_For_With_Multi_Ip(self):
        result = get_ip(self.reqeust_with_X_Forwarded_For_With_Multi_IP)
        excepted = "127.0.0.1"
        self.assertEqual(result, excepted)

    def test_get_ip_Invalid_Headers(self):
        result = get_ip(self.reqeust_with_Invalid_Headers)
        excepted = None
        self.assertEqual(result, excepted)
