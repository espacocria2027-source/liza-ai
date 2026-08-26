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

    # ------------------------------------------------------
    # Se nenhum prompt foi enviado pelo Android,
    # usamos o sistema antigo como fallback.
    # ------------------------------------------------------

    if not prompt:

        contexto = context_manager.build(
            usuario
        )

        prompt = criar_prompt(
            contexto,
            mensagem
        )


    # ======================================================
    # NORMALIZAR PROMPT
    # ======================================================
    #
    # O Android pode enviar o contexto como uma STRING.
    #
    # Os providers, porém, esperam uma LISTA de mensagens.
    #
    # Transformamos:
    #
    #     "contexto completo..."
    #
    # em:
    #
    #     [
    #         {
    #             "role": "system",
    #             "content": "contexto completo..."
    #         },
    #         {
    #             "role": "user",
    #             "content": "mensagem"
    #         }
    #     ]
    #
    # ------------------------------------------------------

    if isinstance(
        prompt,
        str
    ):

        prompt = [

            {

                "role":
                    "system",

                "content":
                    prompt

            },

            {

                "role":
                    "user",

                "content":
                    mensagem

            }

        ]


    # ======================================================
    # VALIDAR PROMPT
    # ======================================================

    if not isinstance(
        prompt,
        list
    ):

        print(
            "⚠ Prompt inválido."
        )

        prompt = [

            {

                "role":
                    "system",

                "content":
                    str(prompt)

            },

            {

                "role":
                    "user",

                "content":
                    mensagem

            }

        ]


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

    print(
        "Quantidade de mensagens:",
        len(prompt)
    )


    # ======================================================
    # DEBUG DAS MENSAGENS
    # ======================================================

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


            # ----------------------------------------------
            # DETECTAR CONHECIMENTO DAS PERSONAS
            # ----------------------------------------------

            content_text = str(
                content
            ).lower()


            if "cibely" in content_text:

                print(
                    "✅ CONTEXTO DE CIBELY ENCONTRADO"
                )


            if "beto" in content_text:

                print(
                    "✅ CONTEXTO DE BETO ENCONTRADO"
                )


            if "rony" in content_text:

                print(
                    "✅ CONTEXTO DE RONY ENCONTRADO"
                )


        else:

            print(
                "⚠ Mensagem não é um objeto válido."
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
    # FALLBACK
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
    # NORMALIZAR PROMPT
    # ======================================================

    if isinstance(
        prompt,
        str
    ):

        prompt = [

            {

                "role":
                    "system",

                "content":
                    prompt

            },

            {

                "role":
                    "user",

                "content":
                    mensagem

            }

        ]


    # ======================================================
    # VALIDAR PROMPT
    # ======================================================

    if not isinstance(
        prompt,
        list
    ):

        prompt = [

            {

                "role":
                    "system",

                "content":
                    str(prompt)

            },

            {

                "role":
                    "user",

                "content":
                    mensagem

            }

        ]


    # ======================================================
    # DEBUG
    # ======================================================

    print("=" * 60)
    print("PROMPT ENVIADO AO STREAM")
    print("=" * 60)

    print(
        "Tipo:",
        type(prompt)
    )

    print(
        "Quantidade de mensagens:",
        len(prompt)
    )


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

        # --------------------------------------------------
        # GARANTIR STRING
        # --------------------------------------------------

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