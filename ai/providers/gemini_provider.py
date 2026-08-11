"""
L.I.Z.A. Gemini Provider
"""

import os

from dotenv import load_dotenv
from google import genai

from ai.providers.base_provider import BaseProvider
from ai.models.model_manager import models


class GeminiProvider(BaseProvider):

    def __init__(self):

        load_dotenv(override=True)

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise RuntimeError(
                "GEMINI_API_KEY não encontrada."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    # ==================================================
    # MÉTODO INTERNO
    # ==================================================

    def _generate(
        self,
        model: str,
        messages: list
    ) -> str:

        print("=" * 60)
        print("Gemini")
        print("Modelo:", model)
        print("=" * 60)

        system_instruction = ""
        contents = []

        for message in messages:

            role = message.get(
                "role",
                "user"
            )

            content = message.get(
                "content",
                ""
            )

            if role == "system":

                system_instruction += (
                    content + "\n\n"
                )

            elif role == "assistant":

                contents.append({

                    "role": "model",

                    "parts": [
                        {
                            "text": content
                        }
                    ]

                })

            else:

                contents.append({

                    "role": "user",

                    "parts": [
                        {
                            "text": content
                        }
                    ]

                })

        config = None

        if system_instruction.strip():

            config = {
                "system_instruction":
                    system_instruction.strip()
            }

        response = self.client.models.generate_content(

            model=model,

            contents=contents,

            config=config

        )

        return response.text or ""

    # ==================================================
    # STREAMING
    # ==================================================

    def _generate_stream(
        self,
        model: str,
        messages: list
    ):

        print("=" * 60)
        print("Gemini Streaming")
        print("Modelo:", model)
        print("=" * 60)

        system_instruction = ""
        contents = []

        for message in messages:

            role = message.get(
                "role",
                "user"
            )

            content = message.get(
                "content",
                ""
            )

            if role == "system":

                system_instruction += (
                    content + "\n\n"
                )

            elif role == "assistant":

                contents.append({

                    "role": "model",

                    "parts": [
                        {
                            "text": content
                        }
                    ]

                })

            else:

                contents.append({

                    "role": "user",

                    "parts": [
                        {
                            "text": content
                        }
                    ]

                })

        config = None

        if system_instruction.strip():

            config = {
                "system_instruction":
                    system_instruction.strip()
            }

        stream = self.client.models.generate_content_stream(

            model=model,

            contents=contents,

            config=config

        )

        for chunk in stream:

            if chunk.text:

                yield chunk.text

    # ==================================================
    # CHAT
    # ==================================================

    def chat(
        self,
        messages
    ):

        return self._generate(

            models.gemini_chat,

            messages

        )

    def chat_stream(
        self,
        messages
    ):

        return self._generate_stream(

            models.gemini_chat,

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

            models.gemini_vision,

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

            models.gemini_fast,

            messages

        )

    # ==================================================
    # RACIOCÍNIO
    # ==================================================

    def reasoning(
        self,
        messages
    ):

        return self._generate(

            models.gemini_reasoning,

            messages

        )

    def reasoning_stream(
        self,
        messages
    ):

        return self._generate_stream(

            models.gemini_reasoning,

            messages

        )