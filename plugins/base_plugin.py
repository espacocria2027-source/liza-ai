"""
====================================================
Plugin Base
====================================================
"""

from abc import ABC
from abc import abstractmethod


class BasePlugin(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    def version(self):
        return "1.0"

    @property
    def enabled(self):
        return True

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def execute(self, action, parameters):
        pass