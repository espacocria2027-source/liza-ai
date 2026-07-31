"""
=========================================
Context Engine
=========================================
"""

from datetime import datetime


class ContextEngine:

    def build(self, usuario, mensagem):

        contexto = {

            "usuario": usuario,

            "mensagem": mensagem,

            "data": datetime.now().strftime("%d/%m/%Y"),

            "hora": datetime.now().strftime("%H:%M:%S"),

            "plataforma": "Android",

            "estado": {

                "online": True,

                "executando": False,

                "modo": "normal"

            }

        }

        return contexto


context_engine = ContextEngine()