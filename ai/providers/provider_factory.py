"""
L.I.Z.A. Provider Factory
"""

from config import AI_PROVIDER

from ai.providers.groq_provider import GroqProvider
from ai.providers.openai_provider import OpenAIProvider
from ai.providers.gemini_provider import GeminiProvider


def create_provider():

    provider = AI_PROVIDER.lower().strip()

    # ==================================================
    # PROVIDER FIXO
    # ==================================================

    if provider == "groq":
        return GroqProvider()

    if provider == "openai":
        return OpenAIProvider()

    if provider == "gemini":
        return GeminiProvider()

    # ==================================================
    # AUTOMÁTICO
    # ==================================================

    if provider == "auto":
        return ProviderRouter()

    raise RuntimeError(
        f"Provider '{AI_PROVIDER}' não encontrado."
    )


class ProviderRouter:

    def __init__(self):

        self.providers = []

        # ==================================================
        # OPENAI
        # ==================================================

        try:

            self.providers.append(
                OpenAIProvider()
            )

            print(
                "✅ OpenAI disponível."
            )

        except Exception as e:

            print(
                f"⚠ OpenAI indisponível: {e}"
            )

        # ==================================================
        # GROQ
        # ==================================================

        try:

            self.providers.append(
                GroqProvider()
            )

            print(
                "✅ Groq disponível."
            )

        except Exception as e:

            print(
                f"⚠ Groq indisponível: {e}"
            )

        # ==================================================
        # GEMINI
        # ==================================================

        try:

            self.providers.append(
                GeminiProvider()
            )

            print(
                "✅ Gemini disponível."
            )

        except Exception as e:

            print(
                f"⚠ Gemini indisponível: {e}"
            )

        # ==================================================
        # NENHUM PROVIDER
        # ==================================================

        if not self.providers:

            raise RuntimeError(
                "Nenhum provedor de IA está disponível."
            )

    # ==================================================
    # CHAT
    # ==================================================

    def chat(
        self,
        messages
    ):

        last_error = None

        for provider in self.providers:

            try:

                print(
                    "Tentando:",
                    provider.__class__.__name__
                )

                return provider.chat(
                    messages
                )

            except Exception as e:

                last_error = e

                print(
                    "Falha:",
                    provider.__class__.__name__,
                    str(e)
                )

        raise RuntimeError(
            f"Todos os providers falharam: {last_error}"
        )

    # ==================================================
    # STREAMING
    # ==================================================

    def chat_stream(
        self,
        messages
    ):

        last_error = None

        for provider in self.providers:

            try:

                print(
                    "Streaming:",
                    provider.__class__.__name__
                )

                for token in provider.chat_stream(
                    messages
                ):

                    yield token

                return

            except Exception as e:

                last_error = e

                print(
                    "Falha no streaming:",
                    provider.__class__.__name__,
                    str(e)
                )

        raise RuntimeError(
            f"Todos os providers falharam: {last_error}"
        )

    # ==================================================
    # FAST
    # ==================================================

    def fast(
        self,
        messages
    ):

        last_error = None

        for provider in self.providers:

            try:

                return provider.fast(
                    messages
                )

            except Exception as e:

                last_error = e

        raise RuntimeError(
            f"Todos os providers falharam: {last_error}"
        )

    # ==================================================
    # REASONING
    # ==================================================

    def reasoning(
        self,
        messages
    ):

        last_error = None

        for provider in self.providers:

            try:

                return provider.reasoning(
                    messages
                )

            except Exception as e:

                last_error = e

        raise RuntimeError(
            f"Todos os providers falharam: {last_error}"
        )

    # ==================================================
    # REASONING STREAMING
    # ==================================================

    def reasoning_stream(
        self,
        messages
    ):

        last_error = None

        for provider in self.providers:

            try:

                for token in provider.reasoning_stream(
                    messages
                ):

                    yield token

                return

            except Exception as e:

                last_error = e

        raise RuntimeError(
            f"Todos os providers falharam: {last_error}"
        )

    # ==================================================
    # VISÃO
    # ==================================================

    def vision(
        self,
        messages
    ):

        last_error = None

        for provider in self.providers:

            try:

                return provider.vision(
                    messages
                )

            except Exception as e:

                last_error = e

        raise RuntimeError(
            f"Todos os providers falharam: {last_error}"
        )