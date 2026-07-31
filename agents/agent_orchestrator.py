"""
====================================================
Agent Orchestrator
====================================================
"""

from agents.agent_manager import agent_manager
from agents.response_builder import response_builder


class AgentOrchestrator:

    def execute(self, usuario, mensagem, agent_names):

        responses = []

        for name in agent_names:

            response = agent_manager.execute(

                name,

                usuario,

                mensagem

            )

            responses.append(response)

        return response_builder.merge(

            responses

        )


orchestrator = AgentOrchestrator()