"""
=========================================
L.I.Z.A Context Manager
=========================================
"""

from ai.memory_service import carregar_memoria


class ContextManager:

    def __init__(self):
        pass

    def build(self, usuario):

        contexto = {

            "history": carregar_memoria(usuario),

            "profile": {},

            "emotion": "normal",

            "facts": []

        }

        return contexto


context_manager = ContextManager()