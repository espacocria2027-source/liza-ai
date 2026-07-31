"""
====================================================
L.I.Z.A Decision Engine
====================================================
"""

from agents.agent_manager import agent_manager
from ai.decision.ai_intent_detector import detect


class DecisionEngine:

    def __init__(self):
        pass

    def process(self, usuario: str, mensagem: str) -> dict:
        """
        Processa uma mensagem do usuário e escolhe
        qual agente será responsável pela execução.
        """

        try:
            resultado = detect(mensagem)

        except Exception as e:
            return {
                "type": "error",
                "text": f"Erro ao detectar intenção: {str(e)}"
            }

        intent = resultado.get("intent", "chat").lower()

        # ===============================
        # Conversa normal
        # ===============================

        if intent == "chat":

            return agent_manager.execute(
                "chat",
                usuario,
                mensagem
            )

        # ===============================
        # Programação
        # ===============================

        elif intent in [
            "programming",
            "code",
            "developer"
        ]:

            return agent_manager.execute(
                "programmer",
                usuario,
                mensagem
            )

        # ===============================
        # Controle Android
        # ===============================

        elif intent in [
            "action",
            "android",
            "device"
        ]:

            return agent_manager.execute(
                "android",
                usuario,
                mensagem
            )

        # ===============================
        # Pesquisa
        # ===============================

        elif intent == "search":

            return agent_manager.execute(
                "search",
                usuario,
                mensagem
            )

        # ===============================
        # Automações
        # ===============================

        elif intent == "automation":

            return agent_manager.execute(
                "automation",
                usuario,
                mensagem
            )

        # ===============================
        # Visão Computacional
        # ===============================

        elif intent == "vision":

            return agent_manager.execute(
                "vision",
                usuario,
                mensagem
            )

        # ===============================
        # Assistente Pessoal
        # ===============================

        elif intent == "assistant":

            return agent_manager.execute(
                "assistant",
                usuario,
                mensagem
            )

        # ===============================
        # Música
        # ===============================

        elif intent == "music":

            return agent_manager.execute(
                "music",
                usuario,
                mensagem
            )

        # ===============================
        # Agenda
        # ===============================

        elif intent == "calendar":

            return agent_manager.execute(
                "calendar",
                usuario,
                mensagem
            )

        # ===============================
        # Fallback
        # ===============================

        return agent_manager.execute(
            "chat",
            usuario,
            mensagem
        )


decision_engine = DecisionEngine()