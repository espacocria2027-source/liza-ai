"""
L.I.Z.A. Mistral Provider
"""

import os

from dotenv import load_dotenv
from mistralai.client import Mistral

from ai.providers.base_provider import BaseProvider


class MistralProvider(BaseProvider):

    def __init__(self):

        load_dotenv(override=True)

        api_key = os.getenv(
            "MISTRAL_API_KEY"
        )

        if not api_key:

            raise RuntimeError(
                "MISTRAL_API_KEY não encontrada."
            )

        self.client = Mistral(
            api_key=api_key
        )

        # ==================================================
        # MODELOS
        # ==================================================

        self.chat_model = (
            "mistral-small-latest"
        )

        self.fast_model = (
            "mistral-small-latest"
        )

        self.reasoning_model = (
            "mistral-small-latest"
        )

        self.vision_model = (
            "mistral-small-latest"
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
        print("Mistral")
        print("Modelo:", model)
        print("=" * 60)

        response = (
            self.client.chat.complete(

                model=model,

                messages=messages,

                temperature=temperature,

                max_tokens=max_tokens
            )
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
        print("Mistral Streaming")
        print("Modelo:", model)
        print("=" * 60)


        stream = (
            self.client.chat.stream(

                model=model,

                messages=messages,

                temperature=temperature,

                max_tokens=max_tokens
            )
        )


        for event in stream:

            if not event.data.choices:

                continue


            delta = (
                event
                .data
                .choices[0]
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

            self.chat_model,

            messages
        )


    def chat_stream(
        self,
        messages
    ):

        return self._generate_stream(

            self.chat_model,

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

            self.fast_model,

            messages,

            temperature=0.3,

            max_tokens=2048
        )


    # ==================================================
    # RACIOCÍNIO
    # ==================================================

    def reasoning(
        self,
        messages
    ):

        return self._generate(

            self.reasoning_model,

            messages,

            temperature=0.2,

            max_tokens=8192
        )


    def reasoning_stream(
        self,
        messages
    ):

        return self._generate_stream(

            self.reasoning_model,

            messages,

            temperature=0.2,

            max_tokens=8192
        )


    # ==================================================
    # VISÃO
    # ==================================================

    def vision(
        self,
        messages
    ):

        return self._generate(

            self.vision_model,

            messages
        )