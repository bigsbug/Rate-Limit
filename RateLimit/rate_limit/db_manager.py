import imp
import redis
from rate_limit.load_config import load_redis_config


class Redis:
    host: str

    def __new__(cls) -> None:
        if not hasattr(Redis, "_ins"):
            cls._ins = super().__new__(cls)
        return cls._ins

    def __init__(self) -> None:
        self.load_config()
        print(self.host, self.key_prefix)

    def load_config(self):
        self.host, self.key_prefix = load_redis_config()
