

import os

from core.context_manager import context_manager

from ai.prompt_builder import criar_prompt

from ai.providers.model_provider import provider

from ai.memory_service import salvar_memoria

from ai.learning.learning_service import learning

# ==========================================================
# Conversa tradicional
# ==========================================================

def conversar(
    usuario: str,
    mensagem: str
) -> str:

    print("=" * 60)
    print("Conversation Service")
    print("ENV:", repr(os.getenv("GROQ_API_KEY")))
    print("Provider:", provider)
    print("=" * 60)

    contexto = context_manager.build(usuario)

    prompt = criar_prompt(
        contexto,
        mensagem
    )

    resposta = provider.chat(
        prompt
    )

    salvar_memoria(
        usuario,
        mensagem,
        resposta
    )

    learning.learn(
        usuario,
        mensagem
    )

    return resposta


# ==========================================================
# Conversa com Streaming
# ==========================================================

def conversar_stream(
    usuario: str,
    prompt: str,
    mensagem: str
):

    print("=" * 60)
    print("Conversation Service (STREAM)")
    print("=" * 60)

    # Se o Android não enviar o prompt,
    # monta normalmente no servidor.
    if not prompt:

        contexto = context_manager.build(usuario)

        prompt = criar_prompt(
            contexto,
            mensagem
        )

    resposta_completa = ""

    for token in provider.chat_stream(prompt):

        resposta_completa += token

        yield token

    salvar_memoria(
        usuario,
        mensagem,
        resposta_completa
    )

    learning.learn(
        usuario,
        mensagem
    )