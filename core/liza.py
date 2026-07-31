"""
====================================================
L.I.Z.A CORE
====================================================
"""

from core.state import state
from core.services import services

from core.event_bus import event_bus
from core import events


class Liza:

    def process(self, usuario, mensagem):

        state.user = usuario

        event_bus.emit(

            events.MESSAGE_RECEIVED,

            {

                "usuario": usuario,

                "mensagem": mensagem

            }

        )

        resposta = services.decision.process(

            usuario,

            mensagem

        )

        event_bus.emit(

            events.MESSAGE_RESPONSE,

            resposta

        )

        return resposta


liza = Liza()