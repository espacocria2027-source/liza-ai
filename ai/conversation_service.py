import os

from core.context_manager import context_manager

from ai.prompt_builder import criar_prompt

from ai.providers.model_provider import provider

from ai.memory_service import salvar_memoria

from ai.learning.learning_service import learning


# ==========================================================
# CONVERSA TRADICIONAL
# ==========================================================

def conversar(
    usuario: str,
    mensagem: str
) -> str:

    print("=" * 60)
    print("Conversation Service")

    # ======================================================
    # SEGURANÇA
    # ======================================================

    print(
        "GROQ_API_KEY configurada:",
        bool(
            os.getenv(
                "GROQ_API_KEY"
            )
        )
    )

    print(
        "Provider:",
        provider
    )

    print("=" * 60)


    # ------------------------------------------------------
    # CONTEXTO
    # ------------------------------------------------------

    contexto = context_manager.build(
        usuario
    )


    # ------------------------------------------------------
    # PROMPT
    # ------------------------------------------------------

    prompt = criar_prompt(
        contexto,
        mensagem
    )


    # ------------------------------------------------------
    # PROVIDER
    # ------------------------------------------------------

    resposta = provider.chat(
        prompt
    )


    # ======================================================
    # DEBUG DA RESPOSTA
    # ======================================================

    print("=" * 60)
    print("RESPOSTA RECEBIDA DO PROVIDER")
    print("=" * 60)

    print("repr:")
    print(
        repr(
            resposta
        )
    )

    print("=" * 60)

    print("texto:")
    print(
        resposta
    )

    print("=" * 60)


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


    # ------------------------------------------------------
    # RETORNO
    # ------------------------------------------------------

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
    print("=" * 60)


    # ------------------------------------------------------
    # SE O ANDROID NÃO ENVIOU O PROMPT
    # ------------------------------------------------------

    if not prompt:

        contexto = context_manager.build(
            usuario
        )

        prompt = criar_prompt(
            contexto,
            mensagem
        )


    # ------------------------------------------------------
    # RESPOSTA COMPLETA
    # ------------------------------------------------------

    resposta_completa = ""


    # ------------------------------------------------------
    # STREAM
    # ------------------------------------------------------

    for token in provider.chat_stream(
        prompt
    ):

        # Garantimos que o token seja string
        if token is None:
            continue


        token = str(
            token
        )


        resposta_completa += token


        yield token


    # ======================================================
    # DEBUG DO STREAM
    # ======================================================

    print("=" * 60)
    print("RESPOSTA COMPLETA DO STREAM")
    print("=" * 60)

    print("repr:")

    print(
        repr(
            resposta_completa
        )
    )

    print("=" * 60)

    print("texto:")

    print(
        resposta_completa
    )

    print("=" * 60)


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