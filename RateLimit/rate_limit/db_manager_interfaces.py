from abc import ABC, abstractclassmethod
from rate_limit.load_config_interface import ConfigLoderInterface


class DBManagerInterface(ABC):
    def connect(self):
        ...

    def close(self):
        ...

    def instance(self):
        ...


class PerformActionDBInterface(ABC):
    @abstractclassmethod
    def set_db(self, DB: DBManagerInterface) -> None:
        ...

    @abstractclassmethod
    def set_expire(self, key, value):
        ...

    @abstractclassmethod
    def show_ttl(self, key):
        ...

    @abstractclassmethod
    def new_view(self, key) -> str:
        ...

    @abstractclassmethod
    def show_view(self, key) -> str:
        ...

    @abstractclassmethod
    def add_to_whitelist(self, target) -> bool:
        ...

    @abstractclassmethod
    def is_in_whitelist(self, target) -> bool:
        ...

    @abstractclassmethod
    def remove_from_whitelist(self, target) -> bool:
        ...

    @abstractclassmethod
    def add_to_blacklist(self, target) -> bool:
        ...

    @abstractclassmethod
    def is_in_blacklist(self, target) -> bool:
        ...

    @abstractclassmethod
    def remove_from_blacklist(self, target) -> bool:
        ...


class RateLimiterInterface(ABC):
    @abstractclassmethod
    def load_config(self):
        ...

    def set_db(self, db_actioner: PerformActionDBInterface):
        ...

    @abstractclassmethod
    def get_rate(self, request):
        ...

    @abstractclassmethod
    def max_rate(self):
        ...

    @abstractclassmethod
    def new_view(self, request):
        ...

    @abstractclassmethod
    def expireing(self, key):
        ...
