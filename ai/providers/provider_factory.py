import os

from ai.providers.groq_provider import GroqProvider


def create_provider():

    provider = os.getenv("AI_PROVIDER", "groq").lower()

    if provider == "groq":
        return GroqProvider()

    raise ValueError(
        f"Provider '{provider}' não encontrado."
    )