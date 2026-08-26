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
    prompt,
    mensagem: str
) -> str:

    print("=" * 60)
    print("Conversation Service")
    print("=" * 60)


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


    # ======================================================
    # PROMPT
    # ======================================================
    #
    # Se o Android enviou um prompt completo,
    # usamos exatamente esse prompt.
    #
    # Se não enviou, criamos um prompt localmente
    # usando o sistema antigo.
    # ======================================================

    if not prompt:

        contexto = context_manager.build(
            usuario
        )

        prompt = criar_prompt(
            contexto,
            mensagem
        )


    # ======================================================
    # DEBUG DO PROMPT
    # ======================================================

    print("=" * 60)
    print("PROMPT ENVIADO AO PROVIDER")
    print("=" * 60)

    print(
        "Tipo:",
        type(prompt)
    )


    # ======================================================
    # VERIFICAR ESTRUTURA
    # ======================================================

    if isinstance(
        prompt,
        list
    ):

        print(
            "Quantidade de mensagens:",
            len(prompt)
        )


        for index, item in enumerate(
            prompt
        ):

            print(
                f"Mensagem #{index}:"
            )


            if isinstance(
                item,
                dict
            ):

                print(
                    "role:",
                    item.get(
                        "role"
                    )
                )


                content = item.get(
                    "content",
                    ""
                )


                print(
                    "tamanho:",
                    len(
                        str(
                            content
                        )
                    )
                )


                # ------------------------------------------
                # IDENTIFICAR CONTEXTO DA PERSONA
                # ------------------------------------------

                content_text = str(
                    content
                ).lower()


                if (
                    "cibely" in
                    content_text
                ):

                    print(
                        "✅ CONTEXTO DE CIBELY ENCONTRADO"
                    )


                if (
                    "beto" in
                    content_text
                ):

                    print(
                        "✅ CONTEXTO DE BETO ENCONTRADO"
                    )


                if (
                    "rony" in
                    content_text
                ):

                    print(
                        "✅ CONTEXTO DE RONY ENCONTRADO"
                    )


            else:

                print(
                    "⚠ Item do prompt não é um objeto."
                )


    else:

        print(
            "⚠ Prompt recebido não é uma lista."
        )


    print("=" * 60)


    # ======================================================
    # PROVIDER
    # ======================================================

    resposta = provider.chat(
        prompt
    )


    # ======================================================
    # DEBUG DA RESPOSTA
    # ======================================================

    print("=" * 60)
    print("RESPOSTA RECEBIDA DO PROVIDER")
    print("=" * 60)


    print(
        "repr:"
    )

    print(
        repr(
            resposta
        )
    )


    print("=" * 60)

    print(
        "texto:"
    )

    print(
        resposta
    )


    print("=" * 60)


    # ======================================================
    # MEMÓRIA
    # ======================================================

    salvar_memoria(
        usuario,
        mensagem,
        resposta
    )


    # ======================================================
    # APRENDIZADO
    # ======================================================

    learning.learn(
        usuario,
        mensagem
    )


    # ======================================================
    # RETORNO
    # ======================================================

    return resposta


# ==========================================================
# CONVERSA COM STREAMING
# ==========================================================

def conversar_stream(
    usuario: str,
    prompt,
    mensagem: str
):

    print("=" * 60)
    print("Conversation Service (STREAM)")
    print("=" * 60)


    # ======================================================
    # SE O ANDROID NÃO ENVIOU O PROMPT
    # ======================================================

    if not prompt:

        contexto = context_manager.build(
            usuario
        )

        prompt = criar_prompt(
            contexto,
            mensagem
        )


    # ======================================================
    # DEBUG DO PROMPT
    # ======================================================

    print("=" * 60)
    print("PROMPT ENVIADO AO STREAM")
    print("=" * 60)

    print(
        "Tipo:",
        type(prompt)
    )


    if isinstance(
        prompt,
        list
    ):

        print(
            "Quantidade de mensagens:",
            len(prompt)
        )


    print("=" * 60)


    # ======================================================
    # RESPOSTA COMPLETA
    # ======================================================

    resposta_completa = ""


    # ======================================================
    # STREAM
    # ======================================================

    for token in provider.chat_stream(
        prompt
    ):

        # -----------------------------------------------
        # GARANTIR QUE O TOKEN SEJA STRING
        # -----------------------------------------------

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


    print(
        "repr:"
    )

    print(
        repr(
            resposta_completa
        )
    )


    print("=" * 60)


    print(
        "texto:"
    )

    print(
        resposta_completa
    )


    print("=" * 60)


    # ======================================================
    # MEMÓRIA
    # ======================================================

    salvar_memoria(
        usuario,
        mensagem,
        resposta_completa
    )


    # ======================================================
    # APRENDIZADO
    # ======================================================

    learning.learn(
        usuario,
        mensagem
    )