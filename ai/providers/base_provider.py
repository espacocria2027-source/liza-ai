from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def chat(self, messages):
        pass