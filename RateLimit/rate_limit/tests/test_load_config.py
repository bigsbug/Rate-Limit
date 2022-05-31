from django.test import TestCase
from rate_limit.load_config import DEFAULT_KEY_PREFIX, LoadRedsiSettings
from rate_limit.exceptions import CantFindBackendRedis, InvalidConfig


class LoadRedsiSettings_FindRedisConfigTestCase(TestCase):
    class SettingsWithCACHES:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.redis.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379",
                "KEY_PREFIX": "example",
            }
        }

    class InvalidSettingsWithCACHES:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
                "LOCATION": "redis://127.0.0.1:6379",
                "KEY_PREFIX": "example",
            }
        }

    class SettingsWithRATE_LIMIT:
        RATE_LIMIT = {
            "REDIS": {
                "LOCATION": "redis://127.0.0.1:6379",
                "KEY_PREFIX": "example",
            }
        }

    class InvalidSettingsWithRATE_LIMIT:
        rate_limit = {
            "redis": {
                "location": "redis://127.0.0.1:6379",
                "key_prefix": "example",
            }
        }

    class EmptySettings:
        ...

    def setUp(self) -> None:
        self.settings_with_CACHES = self.SettingsWithCACHES()
        self.settings_with_invalid_CACHES = self.InvalidSettingsWithCACHES()
        self.settings_with_RATE_LIMIT = self.SettingsWithRATE_LIMIT()
        self.settings_with_invalid_RATE_LIMIT = self.InvalidSettingsWithRATE_LIMIT()
        self.empty_settings = self.EmptySettings()

    # Valid Config
    def test_settings_with_RATE_LIMIT(self):
        result = LoadRedsiSettings(self.settings_with_RATE_LIMIT).find_redis_config()
        excepted = {
            "LOCATION": "redis://127.0.0.1:6379",
            "KEY_PREFIX": "example",
        }
        self.assertEqual(result, excepted)

    def test_settings_with_CACHES(self):
        result = LoadRedsiSettings(self.settings_with_CACHES).find_redis_config()
        excepted = {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379",
            "KEY_PREFIX": "example",
        }
        self.assertEqual(result, excepted)

    #  Invalid Config
    def test_settings_with_invalid_RATE_LIMIT(self):
        result = LoadRedsiSettings(
            self.settings_with_invalid_RATE_LIMIT
        ).find_redis_config
        excepted = CantFindBackendRedis
        self.assertRaises(excepted, result)

    def test_settings_with_invalid_CACHES(self):
        result = LoadRedsiSettings(self.settings_with_invalid_CACHES).find_redis_config
        excepted = CantFindBackendRedis
        self.assertRaises(excepted, result)

    def test_empty_settings(self):
        result = LoadRedsiSettings(self.empty_settings).find_redis_config
        excepted = CantFindBackendRedis
        self.assertRaises(excepted, result)


class LoadRedsiSettings_ExtractConfigTestCase(TestCase):
    DEFAULT_KEY_PREFIX = "RATE_LIMIT"

    class SettingsWithCACHES:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.redis.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379",
                "KEY_PREFIX": "example",
            }
        }

    class SettingsWithRATE_LIMIT:
        RATE_LIMIT = {
            "REDIS": {
                "LOCATION": "redis://127.0.0.1:6379",
                "KEY_PREFIX": "example",
            }
        }

    class SettingsWithRATE_LIMITWithoutKEY_PREFIX:
        RATE_LIMIT = {
            "REDIS": {
                "LOCATION": "redis://127.0.0.1:6379",
            }
        }

    def setUp(self) -> None:
        self.valid_settings = [self.SettingsWithCACHES(), self.SettingsWithRATE_LIMIT]
        self.valid_settings_without_KEY_PREFIX = (
            self.SettingsWithRATE_LIMITWithoutKEY_PREFIX()
        )

    def test_with_valid_settings(self):
        excepted = excepted = ("redis://127.0.0.1:6379", "example")
        for settings in self.valid_settings:
            result = LoadRedsiSettings(settings).extract_config()
            self.assertEqual(result, excepted)

    def test_settings_with_RATE_LIMIT_and_without_KEY_PREFIX(self):

        result = result = LoadRedsiSettings(
            self.valid_settings_without_KEY_PREFIX
        ).extract_config()
        excepted = ("redis://127.0.0.1:6379", self.DEFAULT_KEY_PREFIX)
        self.assertEqual(result, excepted)
