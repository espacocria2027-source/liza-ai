"""
====================================================
L.I.Z.A Groq Provider
====================================================
"""

import os
from dotenv import load_dotenv
from groq import Groq

from ai.providers.base_provider import BaseProvider
from ai.models.model_manager import models


class GroqProvider(BaseProvider):

    def __init__(self):

        load_dotenv(override=True)

        api_key = os.getenv("GROQ_API_KEY")

        print("=" * 60)
        print("API KEY:", repr(api_key))
        print("Tamanho:", len(api_key) if api_key else 0)
        print("=" * 60)

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY não encontrada."
            )

        self.client = Groq(api_key=api_key)

    def _generate(
        self,
        model: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:

        print("=" * 60)
        print("Modelo:", model)
        print("=" * 60)

        resposta = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return resposta.choices[0].message.content

    # ==========================================
    # Conversa
    # ==========================================

    def chat(self, messages):

        return self._generate(
            models.chat,
            messages
        )

    # ==========================================
    # Visão
    # ==========================================

    def vision(self, messages):

        return self._generate(
            models.vision,
            messages
        )

    # ==========================================
    # Modelo rápido
    # ==========================================

    def fast(self, messages):

        return self._generate(
            models.fast,
            messages,
            temperature=0.3
        )

    # ==========================================
    # Modelo de raciocínio
    # ==========================================

    def reasoning(self, messages):

        return self._generate(
            models.reasoning,
            messages,
            temperature=0.2,
            max_tokens=8192
        )