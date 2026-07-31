"""
=========================================
L.I.Z.A Conversation Service
=========================================
"""

from core.context_manager import context_manager

from ai.prompt_builder import criar_prompt

from ai.providers.model_provider import provider

from ai.memory_service import salvar_memoria

from ai.learning.learning_service import learning


def conversar(usuario: str, mensagem: str) -> str:
    """
    Fluxo completo da conversa da L.I.Z.A.

    1. Carrega todo o contexto do usuário
    2. Monta o prompt
    3. Envia para o modelo de IA
    4. Salva a conversa na memória
    5. Aprende novos fatos
    6. Retorna a resposta
    """

    # ==========================
    # CONTEXTO
    # ==========================

    contexto = context_manager.build(usuario)

    # ==========================
    # PROMPT
    # ==========================

    prompt = criar_prompt(
        contexto,
        mensagem
    )

    # ==========================
    # IA
    # ==========================

    resposta = provider.chat(prompt)

    # ==========================
    # MEMÓRIA
    # ==========================

    salvar_memoria(
        usuario,
        mensagem,
        resposta
    )

    # ==========================
    # APRENDIZADO
    # ==========================

    learning.learn(
        usuario,
        mensagem
    )

    # ==========================
    # RESPOSTA
    # ==========================

    return resposta