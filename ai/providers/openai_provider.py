"""
L.I.Z.A. OpenAI Provider
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from ai.providers.base_provider import BaseProvider
from ai.models.model_manager import models


class OpenAIProvider(BaseProvider):

    def __init__(self):

        load_dotenv(override=True)

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:

            raise RuntimeError(
                "OPENAI_API_KEY não encontrada."
            )

        self.client = OpenAI(
            api_key=api_key
        )

    # ==================================================
    # MÉTODO INTERNO
    # ==================================================

    def _generate(
        self,
        model: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:

        print("=" * 60)
        print("OpenAI")
        print("Modelo:", model)
        print("=" * 60)

        response = self.client.chat.completions.create(

            model=model,

            messages=messages,

            temperature=temperature,

            max_tokens=max_tokens

        )

        return (
            response.choices[0]
            .message
            .content
            or ""
        )

    # ==================================================
    # STREAMING
    # ==================================================

    def _generate_stream(
        self,
        model: str,
        messages: list,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ):

        print("=" * 60)
        print("OpenAI Streaming")
        print("Modelo:", model)
        print("=" * 60)

        stream = self.client.chat.completions.create(

            model=model,

            messages=messages,

            temperature=temperature,

            max_tokens=max_tokens,

            stream=True

        )

        for chunk in stream:

            if not chunk.choices:
                continue

            delta = (
                chunk.choices[0]
                .delta
                .content
            )

            if delta:

                yield delta

    # ==================================================
    # CHAT
    # ==================================================

    def chat(
        self,
        messages
    ):

        return self._generate(

            models.openai_chat,

            messages

        )

    def chat_stream(
        self,
        messages
    ):

        return self._generate_stream(

            models.openai_chat,

            messages

        )

    # ==================================================
    # VISÃO
    # ==================================================

    def vision(
        self,
        messages
    ):

        return self._generate(

            models.openai_vision,

            messages

        )

    # ==================================================
    # FAST
    # ==================================================

    def fast(
        self,
        messages
    ):

        return self._generate(

            models.openai_fast,

            messages,

            temperature=0.3

        )

    # ==================================================
    # RACIOCÍNIO
    # ==================================================

    def reasoning(
        self,
        messages
    ):

        return self._generate(

            models.openai_reasoning,

            messages,

            temperature=0.2,

            max_tokens=8192

        )

    def reasoning_stream(
        self,
        messages
    ):

        return self._generate_stream(

            models.openai_reasoning,

            messages,

            temperature=0.2,

            max_tokens=8192

        )