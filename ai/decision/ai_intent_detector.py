"""
====================================================
L.I.Z.A AI Intent Detector
====================================================
"""

import json
import re

from ai.providers.model_provider import provider


SYSTEM_PROMPT = """
Você é o classificador de intenções da L.I.Z.A.

Sua única tarefa é classificar a intenção da mensagem.

Responda APENAS um JSON válido.

Nunca escreva explicações.

Nunca utilize markdown.

Nunca utilize ```json.

As intenções permitidas são:

- chat
- action
- programming

Regras:

chat
- Conversas
- Perguntas
- Explicações
- Curiosidades
- História
- Matemática
- Ciências
- Estudos
- Saudações

programming
- Código
- Python
- Java
- Kotlin
- HTML
- CSS
- JavaScript
- APIs
- Banco de dados
- Programação

action
- Abrir aplicativos
- Abrir YouTube
- Abrir Spotify
- Abrir Google
- WhatsApp
- Ligações
- Configurações
- Volume
- Android

Exemplos

Mensagem:
Olá

Resposta:

{
    "intent":"chat",
    "action":"",
    "parameters":{}
}

Mensagem:
Quem descobriu o Brasil?

Resposta:

{
    "intent":"chat",
    "action":"",
    "parameters":{}
}

Mensagem:
Explique herança em Python.

Resposta:

{
    "intent":"programming",
    "action":"",
    "parameters":{}
}

Mensagem:
Abra o Spotify.

Resposta:

{
    "intent":"action",
    "action":"OPEN_SPOTIFY",
    "parameters":{}
}

Retorne SOMENTE o JSON.
"""


def detect(message: str):

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

    try:

        resposta = provider.reasoning(messages)

        print("\n========== INTENT DETECTOR ==========")
        print(resposta)
        print("=====================================\n")

        texto = resposta.strip()

        # Remove markdown caso o modelo responda ```json

        texto = re.sub(
            r"^```json",
            "",
            texto,
            flags=re.IGNORECASE
        )

        texto = texto.replace(
            "```",
            ""
        ).strip()

        resultado = json.loads(texto)

        return {

            "intent": resultado.get(
                "intent",
                "chat"
            ).lower(),

            "action": resultado.get(
                "action",
                ""
            ),

            "parameters": resultado.get(
                "parameters",
                {}
            )

        }

    except Exception as e:

        print("\n========== ERRO INTENT ==========")
        print(e)
        print("=================================\n")

        return {

            "intent": "chat",

            "action": "",

            "parameters": {}

        }