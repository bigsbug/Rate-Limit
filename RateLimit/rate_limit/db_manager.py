from rate_limit.db_manager_interfaces import DBManager
from rate_limit.load_config_interface import LoadConfigDB
import redis
from rate_limit.load_config import (
    LoadRedisConfigFromCaches,
    LoadRedisConfigFromRateLimit,
)

from django.conf import settings


class Redis(DBManagerInterface):
    host: str
    key_prefix: str

    def load_config(self, config_loder: ConfigLoderInterface):
        self.host, self.key_prefix = config_loder.extract_config()

    def connect(self):
        self.redis = redis.from_url(self.host, decode_responses=True)
        self.redis.ping()
        print(f"Connecting to redis on host {self.host}")

    def close(self):
        self.redis.close()
        print(f"Closing redis connection DB on host {self.host}")

    def instance(self):
        return self.redis

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
