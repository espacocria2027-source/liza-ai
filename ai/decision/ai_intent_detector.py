"""
=========================================
AI Intent Detector
=========================================
"""

import json

from ai.providers.model_provider import provider


SYSTEM_PROMPT = """
Você é um classificador de intenções.

Analise a mensagem do usuário.

Responda APENAS um JSON.

Nunca escreva explicações.

Tipos permitidos:

chat

action

search

automation

Formato:

{
    "intent":"chat",
    "action":"",
    "parameters":{}
}
"""


def detect(message):

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": message
        }

    ]

    resposta = provider.chat(messages)

    try:

        return json.loads(resposta)

    except Exception:

        return {

            "intent": "chat",

            "action": "",

            "parameters": {}

        }