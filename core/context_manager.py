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


    # ======================================================
    # CONSTRUIR CONTEXTO
    # ======================================================

    def build(self, usuario):

        # --------------------------------------------------
        # MEMÓRIA
        # --------------------------------------------------

        history = carregar_memoria(
            usuario
        )


        # --------------------------------------------------
        # LIMITE DO HISTÓRICO
        # --------------------------------------------------

        history = history[
            -MAX_HISTORY_MESSAGES:
        ]


        # --------------------------------------------------
        # CONTEXTO
        # --------------------------------------------------

        contexto = {

            # Identidade do usuário
            "user": usuario,

            # Compatibilidade com código que possa
            # utilizar o nome "usuario"
            "usuario": usuario,

            # Histórico
            "history": history,

            # Perfil
            "profile": {},

            # Estado emocional
            "emotion": "normal",

            # Fatos conhecidos
            "facts": []

        }


        return contexto


context_manager = ContextManager()