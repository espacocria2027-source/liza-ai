"""
====================================================
L.I.Z.A CORE
====================================================
"""

import agents.registry

from core.state import state
from core.services import services

from core.event_bus import event_bus
from core import events


class Liza:

    def process(
        self,
        usuario,
        mensagem,
        prompt=""
    ):

        # ==================================================
        # ESTADO DO USUÁRIO
        # ==================================================

        state.user = usuario


        # ==================================================
        # EVENTO: MENSAGEM RECEBIDA
        # ==================================================

        event_bus.emit(

            events.MESSAGE_RECEIVED,

            {

                "usuario":
                    usuario,

                "mensagem":
                    mensagem,

                "prompt":
                    prompt

            }

        )


        # ==================================================
        # PROCESSAMENTO
        # ==================================================

        resposta = services.decision.process(

            usuario,

            mensagem,

            prompt

        )


        # ==================================================
        # EVENTO: RESPOSTA
        # ==================================================

        event_bus.emit(

            events.MESSAGE_RESPONSE,

            resposta

        )


        # ==================================================
        # RETORNO
        # ==================================================

        return resposta


liza = Liza()