"""
====================================================
L.I.Z.A Decision Engine
====================================================
"""

import detectors.registry

from detectors.detector_manager import detector_manager
from agents.agent_manager import agent_manager


class DecisionEngine:

    def process(self, usuario, mensagem):

        # ==========================================
        # DETECTORES
        # ==========================================

        resultado = detector_manager.detect(

            mensagem

        )

        intent = resultado.get(

            "intent",

            "chat"

        )

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