"""
=========================================
PLUGIN BASE
=========================================
"""

from abc import ABC, abstractmethod


class Plugin(ABC):

    def __init__(self):

        self.name = ""

        self.description = ""

        self.version = "1.0"

    @abstractmethod
    def can_handle(self, action):

        """
        Retorna True se o plugin consegue executar a ação.
        """

        pass

    @abstractmethod
    def execute(self, action, data):

        """
        Executa a ação.
        """

        pass