from agents.base_agent import BaseAgent
from ai.conversation_service import conversar


class ProgrammerAgent(BaseAgent):

    @property
    def name(self):

        return "programmer"

    def execute(self, usuario, mensagem):

        prompt = f"""
Você é especialista em programação.

{mensagem}
"""

        resposta = conversar(
            usuario,
            prompt
        )

        return {

            "type": "chat",

            "text": resposta

        }