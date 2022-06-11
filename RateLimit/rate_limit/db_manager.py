"""Offers Some DB Managers and Creator For Interact With DBs
"""

import redis

from rate_limit.db_manager_interfaces import (
    DBManagerInterface,
    PerformActionDBInterface,
)
from rate_limit.load_config_interface import ConfigLoderInterface

from django.conf import settings


class Redis(DBManagerInterface):
    host: str
    key_prefix: str

    def __init__(self, host: str, key_prefix: str) -> None:
        self.host = host
        self.key_prefix = key_prefix

    def connect(self):
        self.redis = redis.from_url(self.host, decode_responses=True)
        self.redis.ping()
        print(f"Connecting to redis on host {self.host}")

    def close(self):
        self.redis.close()
        print(f"Closing redis connection DB on host {self.host}")

    def instance(self):
        return self.redis


class PerformActionRedis(PerformActionDBInterface):
    def set_db(self, DB: DBManagerInterface) -> None:
        self.db: redis.Redis = DB.instance()
        self.key_prefix = DB.key_prefix
        self.save_pattern = self.key_prefix + ":"

    def set_expire(self, key, time_expire):
        return self.db.expire(self.save_pattern + key, time_expire)

    def show_ttl(self, key):
        return self.db.ttl(self.save_pattern + key)

    def new_view(self, key) -> str:
        key = self.save_pattern + str(key)
        print(key)
        return self.db.incrby(key, 1)

    def show_view(self, key) -> str:
        count_rate = self.db.get(self.save_pattern + str(key))
        return int(count_rate) if count_rate != None else 0

    def add_to_whitelist(self, target) -> bool:
        return self.db.sadd(self.save_pattern + "whitelist", target)

    def is_in_whitelist(self, target) -> bool:
        return self.db.sismember(self.save_pattern + "whitelist", target)

    def remove_from_whitelist(self, target) -> bool:
        ...

    def add_to_blacklist(self, target) -> bool:
        return self.db.sadd(self.save_pattern + "blacklist", target)

    def is_in_blacklist(self, target) -> bool:
        return self.db.sismember(self.save_pattern + "blacklist", target)

    def remove_from_blacklist(self, target) -> bool:
        ...
