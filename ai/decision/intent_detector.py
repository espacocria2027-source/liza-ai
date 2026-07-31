"""
=========================================
AI Intent Detector
=========================================
"""

from ai.providers.model_provider import provider
from ai.decision.parser import parse


SYSTEM_PROMPT = """
Você é um classificador de intenções.

Sua única função é responder um JSON.

Nunca explique.

Nunca use Markdown.

Tipos possíveis:

chat
action
search
automation

Formato obrigatório:

{
  "intent":"",
  "action":"",
  "parameters":{}
}
"""


def detect(message):

    resposta = provider.chat(

        [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": message
            }

        ]

    )

    return parse(resposta)