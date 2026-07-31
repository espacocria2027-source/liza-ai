"""
====================================================
SERVIÇO DE IA
====================================================
"""

import requests

from config import MODEL_CHAT
from ai.prompt_builder import prompt_builder

OLLAMA_URL = "http://localhost:11434/api/chat"


class AIService:

    def __init__(self):
        self.model = MODEL_CHAT

    def chat(self, usuario, history, message):

        messages = prompt_builder.build(
            usuario,
            history,
            message
        )

        messages.extend(history)

        messages.append({
            "role": "user",
            "content": message
        })

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": self.model,
                "messages": messages,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]


ai = AIService()