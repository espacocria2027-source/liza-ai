"""
L.I.Z.A. Provider Factory
"""

import time

from config import AI_PROVIDER

from ai.providers.groq_provider import GroqProvider
from ai.providers.openai_provider import OpenAIProvider
from ai.providers.gemini_provider import GeminiProvider
from ai.providers.mistral_provider import MistralProvider


# ============================================================
# CRIAÇÃO DO PROVIDER
# ============================================================

def create_provider():

    provider = AI_PROVIDER.lower().strip()


    # ========================================================
    # PROVIDER FIXO
    # ========================================================

    if provider == "groq":

        return GroqProvider()


    if provider == "mistral":

        return MistralProvider()


    if provider == "gemini":

        return GeminiProvider()


    if provider == "openai":

        return OpenAIProvider()


    # ========================================================
    # AUTOMÁTICO
    # ========================================================

    if provider == "auto":

        return ProviderRouter()


    # ========================================================
    # PROVIDER INVÁLIDO
    # ========================================================

    raise RuntimeError(
        f"Provider '{AI_PROVIDER}' não encontrado."
    )


# ============================================================
# ROUTER
# ============================================================

class ProviderRouter:


    def __init__(self):

        self.providers = []


        # ====================================================
        # CONFIGURAÇÃO DO COOLDOWN
        # ====================================================

        # 5 minutos

        self.cooldown_seconds = 300


        # Guarda o instante em que cada provider
        # entrou em cooldown.

        self.cooldowns = {}


        # ====================================================
        # GROQ
        # ====================================================

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


        # ====================================================
        # MISTRAL
        # ====================================================

        try:

            self.providers.append(
                MistralProvider()
            )

            print(
                "✅ Mistral disponível."
            )

        except Exception as e:

            print(
                f"⚠ Mistral indisponível: {e}"
            )


        # ====================================================
        # GEMINI
        # ====================================================

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


        # ====================================================
        # OPENAI
        # ====================================================

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


        # ====================================================
        # NENHUM PROVIDER
        # ====================================================

        if not self.providers:

            raise RuntimeError(
                "Nenhum provedor de IA está disponível."
            )


    # ============================================================
    # NOME DO PROVIDER
    # ============================================================

    def _provider_name(
        self,
        provider
    ):

        return provider.__class__.__name__


    # ============================================================
    # IDENTIFICAR LIMITE / QUOTA
    # ============================================================

    def _is_limit_error(
        self,
        error
    ):

        text = str(
            error
        ).lower()


        limit_signals = [

            "429",

            "rate limit",

            "rate_limit",

            "ratelimit",

            "too many requests",

            "quota",

            "quota exceeded",

            "quota_exceeded",

            "tokens per minute",

            "tokens_per_minute",

            "tokens per day",

            "tokens_per_day",

            "daily limit",

            "daily_limit",

            "monthly limit",

            "monthly_limit",

            "usage limit",

            "usage_limit",

            "resource exhausted",

            "resource_exhausted",

            "insufficient quota",

            "insufficient_quota",

            "requests per minute",

            "requests_per_minute"
        ]


        return any(
            signal in text
            for signal in limit_signals
        )


    # ============================================================
    # COOLDOWN
    # ============================================================

    def _is_in_cooldown(
        self,
        provider
    ):

        name = self._provider_name(
            provider
        )


        cooldown_until = (
            self.cooldowns.get(
                name
            )
        )


        # Provider nunca entrou em cooldown

        if cooldown_until is None:

            return False


        now = time.time()


        # Cooldown terminou

        if now >= cooldown_until:

            del self.cooldowns[
                name
            ]


            print(
                f"🔄 Cooldown terminado: {name}"
            )

            print(
                f"🧪 Testando {name} novamente..."
            )


            return False


        # Ainda está em cooldown

        remaining = int(
            cooldown_until - now
        )


        minutes = remaining // 60

        seconds = remaining % 60


        print(
            f"⏳ {name} em cooldown."
        )

        print(
            f"   Tempo restante: "
            f"{minutes}m {seconds}s"
        )


        return True


    # ============================================================
    # ATIVAR COOLDOWN
    # ============================================================

    def _set_cooldown(
        self,
        provider
    ):

        name = self._provider_name(
            provider
        )


        cooldown_until = (
            time.time()
            + self.cooldown_seconds
        )


        self.cooldowns[
            name
        ] = cooldown_until


        print(
            "=============================================="
        )

        print(
            f"🚫 {name} entrou em cooldown."
        )

        print(
            "⏱ Duração: 5 minutos"
        )

        print(
            "🔄 O próximo provider será utilizado."
        )

        print(
            "=============================================="
        )


    # ============================================================
    # CHAT
    # ============================================================

    def chat(
        self,
        messages
    ):

        last_error = None


        for provider in self.providers:

            name = self._provider_name(
                provider
            )


            # ==================================================
            # VERIFICAR COOLDOWN
            # ==================================================

            if self._is_in_cooldown(
                provider
            ):

                continue


            try:

                print(
                    "=============================================="
                )

                print(
                    "🤖 Tentando:",
                    name
                )

                print(
                    "=============================================="
                )


                response = provider.chat(
                    messages
                )


                print(
                    f"✅ Resposta recebida de: {name}"
                )


                return response


            except Exception as e:

                last_error = e


                if self._is_limit_error(
                    e
                ):

                    print(
                        f"⚠ {name} atingiu limite/quota."
                    )


                    self._set_cooldown(
                        provider
                    )


                else:

                    print(
                        f"⚠ Falha em {name}:",
                        str(e)
                    )


                print(
                    "🔄 Tentando próximo provider..."
                )


        raise RuntimeError(

            "Todos os providers falharam. "
            f"Último erro: {last_error}"

        )


    # ============================================================
    # STREAMING
    # ============================================================

    def chat_stream(
        self,
        messages
    ):

        last_error = None


        for provider in self.providers:

            name = self._provider_name(
                provider
            )


            if self._is_in_cooldown(
                provider
            ):

                continue


            try:

                print(
                    "=============================================="
                )

                print(
                    "🎙 Streaming:",
                    name
                )

                print(
                    "=============================================="
                )


                for token in provider.chat_stream(
                    messages
                ):

                    yield token


                print(
                    f"✅ Streaming concluído: {name}"
                )


                return


            except Exception as e:

                last_error = e


                if self._is_limit_error(
                    e
                ):

                    print(
                        f"⚠ {name} atingiu limite durante streaming."
                    )


                    self._set_cooldown(
                        provider
                    )


                else:

                    print(
                        f"⚠ Falha no streaming de {name}:",
                        str(e)
                    )


                print(
                    "🔄 Tentando próximo provider..."
                )


        raise RuntimeError(

            "Todos os providers falharam no streaming. "
            f"Último erro: {last_error}"

        )


    # ============================================================
    # FAST
    # ============================================================

    def fast(
        self,
        messages
    ):

        last_error = None


        for provider in self.providers:

            name = self._provider_name(
                provider
            )


            if self._is_in_cooldown(
                provider
            ):

                continue


            try:

                print(
                    "⚡ Fast:",
                    name
                )


                response = provider.fast(
                    messages
                )


                print(
                    f"✅ Fast respondeu: {name}"
                )


                return response


            except Exception as e:

                last_error = e


                if self._is_limit_error(
                    e
                ):

                    print(
                        f"⚠ {name} atingiu limite no Fast."
                    )


                    self._set_cooldown(
                        provider
                    )


                else:

                    print(
                        f"⚠ Falha no Fast de {name}:",
                        str(e)
                    )


                print(
                    "🔄 Tentando próximo provider..."
                )


        raise RuntimeError(

            "Todos os providers falharam no Fast. "
            f"Último erro: {last_error}"

        )


    # ============================================================
    # REASONING
    # ============================================================

    def reasoning(
        self,
        messages
    ):

        last_error = None


        for provider in self.providers:

            name = self._provider_name(
                provider
            )


            if self._is_in_cooldown(
                provider
            ):

                continue


            try:

                print(
                    "🧠 Reasoning:",
                    name
                )


                response = provider.reasoning(
                    messages
                )


                print(
                    f"✅ Reasoning respondeu: {name}"
                )


                return response


            except Exception as e:

                last_error = e


                if self._is_limit_error(
                    e
                ):

                    print(
                        f"⚠ {name} atingiu limite no Reasoning."
                    )


                    self._set_cooldown(
                        provider
                    )


                else:

                    print(
                        f"⚠ Falha no Reasoning de {name}:",
                        str(e)
                    )


                print(
                    "🔄 Tentando próximo provider..."
                )


        raise RuntimeError(

            "Todos os providers falharam no Reasoning. "
            f"Último erro: {last_error}"

        )


    # ============================================================
    # REASONING STREAMING
    # ============================================================

    def reasoning_stream(
        self,
        messages
    ):

        last_error = None


        for provider in self.providers:

            name = self._provider_name(
                provider
            )


            if self._is_in_cooldown(
                provider
            ):

                continue


            try:

                print(
                    "🧠 Reasoning Streaming:",
                    name
                )


                for token in provider.reasoning_stream(
                    messages
                ):

                    yield token


                print(
                    f"✅ Reasoning Streaming concluído: {name}"
                )


                return


            except Exception as e:

                last_error = e


                if self._is_limit_error(
                    e
                ):

                    print(
                        f"⚠ {name} atingiu limite no "
                        f"Reasoning Streaming."
                    )


                    self._set_cooldown(
                        provider
                    )


                else:

                    print(
                        f"⚠ Falha no Reasoning Streaming "
                        f"de {name}:",
                        str(e)
                    )


                print(
                    "🔄 Tentando próximo provider..."
                )


        raise RuntimeError(

            "Todos os providers falharam no "
            "Reasoning Streaming. "
            f"Último erro: {last_error}"

        )


    # ============================================================
    # VISÃO
    # ============================================================

    def vision(
        self,
        messages
    ):

        last_error = None


        for provider in self.providers:

            name = self._provider_name(
                provider
            )


            if self._is_in_cooldown(
                provider
            ):

                continue


            try:

                print(
                    "👁 Vision:",
                    name
                )


                response = provider.vision(
                    messages
                )


                print(
                    f"✅ Vision respondeu: {name}"
                )


                return response


            except Exception as e:

                last_error = e


                if self._is_limit_error(
                    e
                ):

                    print(
                        f"⚠ {name} atingiu limite na Vision."
                    )


                    self._set_cooldown(
                        provider
                    )


                else:

                    print(
                        f"⚠ Falha na Vision de {name}:",
                        str(e)
                    )


                print(
                    "🔄 Tentando próximo provider..."
                )


        raise RuntimeError(

            "Todos os providers falharam na Vision. "
            f"Último erro: {last_error}"

        )