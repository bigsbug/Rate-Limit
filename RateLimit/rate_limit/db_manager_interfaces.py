from abc import ABC, abstractclassmethod
from rate_limit.load_config_interface import LoadConfigDB


class DBManager(ABC):
    def connect(self):
        ...
    def close(self):
        ...
        
    def load_config(self):
        ...
