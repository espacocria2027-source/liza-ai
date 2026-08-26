from agents.base_agent import BaseAgent
from ai.conversation_service import conversar


class ChatAgent(BaseAgent):

    @property
    def name(self):

        return "chat"


    # ==================================================
    # EXECUTAR
    # ==================================================

    def execute(
        self,
        usuario,
        mensagem,
        prompt=""
    ):

        resposta = conversar(

            usuario,

            prompt,

            mensagem

        )


        return {

            "type":
                "chat",

            "text":
                resposta

        }