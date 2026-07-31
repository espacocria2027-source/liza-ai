from agents.base_agent import BaseAgent
from ai.conversation_service import conversar


class ChatAgent(BaseAgent):

    @property
    def name(self):

        return "chat"

    def execute(self, usuario, mensagem):

        resposta = conversar(
            usuario,
            mensagem
        )

        return {

            "type": "chat",

            "text": resposta

        }