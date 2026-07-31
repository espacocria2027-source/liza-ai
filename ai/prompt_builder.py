from ai.prompt_loader import carregar_prompt


def criar_prompt(contexto, mensagem):

    mensagens = [

        {

            "role": "system",

            "content": carregar_prompt("system.txt")

        }

    ]

    mensagens.extend(

        contexto["history"]

    )

    mensagens.append(

        {

            "role": "user",

            "content": mensagem

        }

    )

    return mensagens