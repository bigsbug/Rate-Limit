from rate_limit.db_manager_interfaces import DBManager
from rate_limit.load_config_interface import LoadConfigDB
import redis
from rate_limit.load_config import (
    LoadRedisConfigFromCaches,
    LoadRedisConfigFromRateLimit,
)

from django.conf import settings


class Redis(DBManager):
    host: str
    key_prefix: str

    def __new__(cls) -> None:
        if not hasattr(Redis, "_ins"):
            cls._ins = super().__new__(cls)
        return cls._ins

    def load_config(self, loader_config: LoadConfigDB):
        self.host, self.key_prefix = loader_config.extract_config()

    def connect(self):
        print(f"Connecting to {self.host}")

    def close(self):
        print(f"closing Connectino DB on port {self.host}")


class PerformActionDB:
    def __init__(self, DB: DBManager) -> None:
        self.db = DB

    def new_view_by_ip(self, ip):
        ...

    def show_view_by_ip(self, ip):
        ...

    def new_view_by_user(self, user):
        ...

    def show_view_by_user(self, user):
        ...

    def add_to_whitelist(self, target):
        ...

    def remove_from_whitelist(self, target):
        ...

    def add_to_blacklist(self, target):
        ...

    def remove_from_blacklist(self, target):
        ...


def DB():
    myredis = Redis()
    redis_config = LoadRedisConfigFromRateLimit(settings)
    myredis.load_config(redis_config)
    myredis.connect()
