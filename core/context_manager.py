"""
L.I.Z.A Context Manager
"""

from ai.memory_service import carregar_memoria


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

MAX_HISTORY_MESSAGES = 10


class ContextManager:

    def __init__(self):
        pass

    def build(self, usuario):

        history = carregar_memoria(
            usuario
        )

        # Mantém somente as mensagens mais recentes
        history = history[
            -MAX_HISTORY_MESSAGES:
        ]

        contexto = {

            "history": history,

            "profile": {},

            "emotion": "normal",

            "facts": []

        }

        return contexto


context_manager = ContextManager()