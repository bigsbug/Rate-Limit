from abc import ABC, abstractclassmethod
from rate_limit.load_config_interface import LoadConfigDB


class DBManagerInterface(ABC):
    def connect(self):
        ...

    def close(self):
        ...
        
    def load_config(self):
        ...

    def instance(self):
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
