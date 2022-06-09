"""Interfaces Of Config Loaders"""

from abc import ABC, abstractclassmethod


class ConfigLoderInterface(ABC):
    @abstractclassmethod
    def find_config(self, settings):
        ...

    @abstractclassmethod
    def extract_config(self):
        ...
