"""
=========================================
L.I.Z.A Planner
=========================================
"""

from ai.providers.model_provider import provider

from ai.planner.parser import parse


SYSTEM_PROMPT = """
Você é um planejador.

Nunca converse.

Nunca explique.

Sua única função é transformar pedidos em um plano.

Responda APENAS JSON.

Formato:

{

    "message":"",

    "steps":[

        {

            "action":"",

            "parameters":{}

        }

    ]

}
"""


class Planner:

    def create(self, mensagem):

        resposta = provider.chat(

            [

                {

                    "role":"system",

                    "content":SYSTEM_PROMPT

                },

                {

                    "role":"user",

                    "content":mensagem

                }

            ]

        )

        return parse(resposta)


planner = Planner()