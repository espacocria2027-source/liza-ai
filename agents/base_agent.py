from abc import ABC, abstractmethod


class BaseAgent(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def execute(self, usuario, mensagem):
        pass