from services.memory_service import (
    carregar_memoria,
    salvar_memoria
)

from services.ai_service import gerar_resposta


def processar_chat(

    usuario: str,

    mensagem: str

):

    historico = carregar_memoria(

        usuario

    )

    resposta = gerar_resposta(

        mensagem,

        historico

    )

    salvar_memoria(

        usuario,

        mensagem,

        resposta

    )

    return resposta