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

            # Conversa
            "chat": "chat",
            "conversation": "chat",
            "assistant": "chat",
            "search": "chat",
            "vision": "chat",
            "automation": "chat",
            "calendar": "chat",
            "music": "chat",

            # Programação
            "programming": "programmer",
            "code": "programmer",
            "developer": "programmer",

            # Android
            "action": "android",
            "android": "android",
            "device": "android"

        }

    def process(self, usuario: str, mensagem: str) -> dict:
        """
        Detecta a intenção do usuário e encaminha
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

        agent = self.intent_map.get(

            intent,

            "chat"

        )

        resposta = agent_manager.execute(

            agent,

            usuario,

            mensagem

        )

        return resposta


decision_engine = DecisionEngine()