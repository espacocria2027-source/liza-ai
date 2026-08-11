import os

from core.context_manager import context_manager

from ai.prompt_builder import criar_prompt

from ai.providers.model_provider import provider

from ai.memory_service import salvar_memoria

from ai.learning.learning_service import learning


# ==========================================================
# CONFIGURAÇÃO DE CONTEXTO
# ==========================================================

# Quantas mensagens antigas podem ser enviadas para a IA.
# Isso reduz bastante o consumo de tokens.
MAX_HISTORY_MESSAGES = 10


# ==========================================================
# LIMITA O HISTÓRICO
# ==========================================================

def limitar_contexto(contexto: dict) -> dict:

    history = contexto.get(
        "history",
        []
    )

    # Mantém somente as mensagens mais recentes.
    history = history[
        -MAX_HISTORY_MESSAGES:
    ]

    return {
        **contexto,
        "history": history
    }


# ==========================================================
# CONVERSA TRADICIONAL
# ==========================================================

def conversar(
    usuario: str,
    mensagem: str
) -> str:

    print("=" * 60)
    print("Conversation Service")
    print(
        "Provider:",
        provider.__class__.__name__
    )
    print("=" * 60)

    # ------------------------------------------------------
    # CONTEXTO
    # ------------------------------------------------------

    contexto = context_manager.build(
        usuario
    )

    contexto = limitar_contexto(
        contexto
    )

    # ------------------------------------------------------
    # PROMPT
    # ------------------------------------------------------

    prompt = criar_prompt(
        contexto,
        mensagem
    )

    print(
        "Mensagens enviadas para a IA:",
        len(prompt)
    )

    # ------------------------------------------------------
    # IA
    # ------------------------------------------------------

    resposta = provider.chat(
        prompt
    )

    # ------------------------------------------------------
    # MEMÓRIA
    # ------------------------------------------------------

    salvar_memoria(
        usuario,
        mensagem,
        resposta
    )

    # ------------------------------------------------------
    # APRENDIZADO
    # ------------------------------------------------------

    learning.learn(
        usuario,
        mensagem
    )

    return resposta


# ==========================================================
# CONVERSA COM STREAMING
# ==========================================================

def conversar_stream(
    usuario: str,
    prompt: str,
    mensagem: str
):

    print("=" * 60)
    print("Conversation Service (STREAM)")
    print(
        "Provider:",
        provider.__class__.__name__
    )
    print("=" * 60)

    # ------------------------------------------------------
    # SE O ANDROID NÃO ENVIAR O PROMPT,
    # MONTA NORMALMENTE NO SERVIDOR.
    # ------------------------------------------------------

    if not prompt:

        contexto = context_manager.build(
            usuario
        )

        contexto = limitar_contexto(
            contexto
        )

        prompt = criar_prompt(
            contexto,
            mensagem
        )

    # ------------------------------------------------------
    # STREAMING
    # ------------------------------------------------------

    resposta_completa = ""

    for token in provider.chat_stream(
        prompt
    ):

        resposta_completa += token

        yield token

    # ------------------------------------------------------
    # MEMÓRIA
    # ------------------------------------------------------

    salvar_memoria(
        usuario,
        mensagem,
        resposta_completa
    )

    # ------------------------------------------------------
    # APRENDIZADO
    # ------------------------------------------------------

    learning.learn(
        usuario,
        mensagem
    )