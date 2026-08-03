"""
====================================================
L.I.Z.A Decision Engine
====================================================
"""

from agents.agent_manager import agent_manager
from ai.decision.ai_intent_detector import detect


class DecisionEngine:

    def __init__(self):

        self.intent_map = {

            "chat": "chat",

            "programmer": "programmer",

            "android": "android"

        }

    def process(self, usuario: str, mensagem: str) -> dict:
        """
        Detecta a intenção do usuário e envia
        para o agente correto.
        """

        try:

            resultado = detect(mensagem)

        except Exception as e:

            return {

                "type": "error",

                "text": f"Erro ao detectar intenção: {str(e)}"

            }

        intent = resultado.get(

            "intent",

            "chat"

        ).lower()

        # ==========================================
        # ANDROID
        # ==========================================

        if intent == "android":

            return agent_manager.execute(

                "android",

                usuario,

                resultado

            )

        # ==========================================
        # PROGRAMADOR
        # ==========================================

        if intent == "programmer":

            return agent_manager.execute(

                "programmer",

                usuario,

                mensagem

            )

        # ==========================================
        # CHAT
        # ==========================================

        return agent_manager.execute(

            "chat",

            usuario,

            mensagem

        )


decision_engine = DecisionEngine()