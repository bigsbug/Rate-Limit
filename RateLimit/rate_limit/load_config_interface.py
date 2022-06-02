from abc import ABC, abstractclassmethod


class LoadConfigDB(ABC):
    @abstractclassmethod
    def find_config(self, settings):
        ...

    @abstractclassmethod
    def extract_config(self):
        ...
