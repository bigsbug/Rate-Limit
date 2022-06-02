from django.test import TestCase
from rate_limit.load_config import (
    DEFAULT_KEY_PREFIX,
    LoadRedisConfigFromCaches,
    LoadRedisConfigFromRateLimit,
)
from rate_limit.exceptions import CantFindBackendRedis, InvalidConfig


class LoadRedisConfigFromRateLimitTastCase(TestCase):
    class Settings:
        RATE_LIMIT = {
            "REDIS": {
                "LOCATION": "redis://127.0.0.1:6379",
                "KEY_PREFIX": "example",
            }
        }

    class InvalidSettings:
        rate_limit = {
            "redis": {
                "location": "redis://127.0.0.1:6379",
                "key_prefix": "example",
            }
        }

    class SettingsWithoutKEY_PREFIX:
        RATE_LIMIT = {
            "REDIS": {
                "LOCATION": "redis://127.0.0.1:6379",
            }
        }

    class EmptySettings:
        ...

    def setUp(self) -> None:

        self.settings_with_RATE_LIMIT = self.Settings()
        self.valid_settings_without_KEY_PREFIX = self.SettingsWithoutKEY_PREFIX()
        self.settings_with_invalid_RATE_LIMIT = self.InvalidSettings()
        self.empty_settings = self.EmptySettings()

    # Valid Config
    def test_find_config_with_valid_settings(self):
        result = LoadRedisConfigFromRateLimit(
            self.settings_with_RATE_LIMIT
        ).find_config()
        excepted = {
            "LOCATION": "redis://127.0.0.1:6379",
            "KEY_PREFIX": "example",
        }
        self.assertEqual(result, excepted)

    #  Invalid Config
    def test_find_config_with_invalid_settings(self):
        result = LoadRedisConfigFromRateLimit(
            self.settings_with_invalid_RATE_LIMIT
        ).find_config
        excepted = CantFindBackendRedis
        self.assertRaises(excepted, result)

    def test_find_config_with_empty_settings(self):
        result = LoadRedisConfigFromRateLimit(self.empty_settings).find_config
        excepted = CantFindBackendRedis
        self.assertRaises(excepted, result)

    def test_extract_config_with_valid_settings(self):
        excepted = excepted = ("redis://127.0.0.1:6379", "example")
        result = LoadRedisConfigFromRateLimit(
            self.settings_with_RATE_LIMIT
        ).extract_config()
        self.assertEqual(result, excepted)

    def test_extract_config_without_KEY_PREFIX(self):

        result = result = LoadRedisConfigFromRateLimit(
            self.valid_settings_without_KEY_PREFIX
        ).extract_config()
        excepted = ("redis://127.0.0.1:6379", DEFAULT_KEY_PREFIX)
        self.assertEqual(result, excepted)


class LoadRedisConfigFromCachesTestCase(TestCase):
    class Settings:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.redis.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379",
                "KEY_PREFIX": "example",
            }
        }

    class SettingsWithoutKeyPrefix:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.redis.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379",
            }
        }

    class InvalidSettings:
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
                "LOCATION": "redis://127.0.0.1:6379",
                "KEY_PREFIX": "example",
            }
        }

    class EmptySettings:
        ...

    def setUp(self) -> None:
        self.settings_with_CACHES = self.Settings()
        self.settings_without_KEY_PREFIX = self.SettingsWithoutKeyPrefix()
        self.settings_with_invalid_CACHES = self.InvalidSettings()
        self.empty_settings = self.EmptySettings()

    # Valid Config
    def test_find_config_with_valid_settings(self):
        result = LoadRedisConfigFromCaches(self.settings_with_CACHES).find_config()
        excepted = {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379",
            "KEY_PREFIX": "example",
        }
        self.assertEqual(result, excepted)

    #  Invalid Config
    def test_find_config_with_invalid_settings(self):
        result = LoadRedisConfigFromCaches(
            self.settings_with_invalid_CACHES
        ).find_config
        excepted = CantFindBackendRedis
        self.assertRaises(excepted, result)

    def test_find_config_with_empty_settings(self):
        result = LoadRedisConfigFromCaches(self.empty_settings).find_config
        excepted = CantFindBackendRedis
        self.assertRaises(excepted, result)

    def test_extract_config_with_valid_settings(self):
        excepted = excepted = ("redis://127.0.0.1:6379", "example")
        result = LoadRedisConfigFromCaches(self.settings_with_CACHES).extract_config()
        self.assertEqual(result, excepted)

    def test_extract_config_without_KEY_PREFIX(self):

        result = result = LoadRedisConfigFromCaches(
            self.settings_without_KEY_PREFIX
        ).extract_config()
        excepted = ("redis://127.0.0.1:6379", DEFAULT_KEY_PREFIX)
        self.assertEqual(result, excepted)
