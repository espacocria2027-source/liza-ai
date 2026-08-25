from ai.prompt_loader import carregar_prompt


def criar_prompt(
    contexto,
    mensagem
):

    # ==================================================
    # IDENTIDADE DO USUÁRIO
    # ==================================================

    usuario = contexto.get(
        "user",
        ""
    )

    if not usuario:

        usuario = contexto.get(
            "usuario",
            ""
        )

    if not usuario:

        usuario = "usuário"


    # ==================================================
    # PROMPT PRINCIPAL
    # ==================================================

    system_prompt = carregar_prompt(
        "system.txt"
    )


    # ==================================================
    # CONTEXTO DE IDENTIDADE
    # ==================================================

    identidade = f"""
==================================================
IDENTIDADE DO USUÁRIO
==================================================

Nome do usuário:
{usuario}

INSTRUÇÕES:

- Você sabe o nome do usuário.
- Use o nome ocasionalmente e de maneira natural.
- Não repita o nome em todas as respostas.
- Não force o uso do nome quando não fizer sentido.
- Use o nome especialmente quando estiver
  cumprimentando, chamando a atenção do usuário,
  dando uma explicação pessoal ou quando isso
  tornar a conversa mais natural.
- Nunca invente outro nome para o usuário.
- Se o nome disponível for apenas "usuário",
  não trate "usuário" como se fosse um nome real.
==================================================
"""


    # ==================================================
    # SYSTEM
    # ==================================================

    mensagens = [

        {

            "role": "system",

            "content":
                system_prompt
                + "\n\n"
                + identidade

        }

    ]


    # ==================================================
    # HISTÓRICO
    # ==================================================

    history = contexto.get(
        "history",
        []
    )


    if history:

        mensagens.extend(
            history
        )


    # ==================================================
    # MENSAGEM ATUAL
    # ==================================================

    mensagens.append(

        {

            "role": "user",

            "content":
                mensagem

        }

    )


    return mensagens