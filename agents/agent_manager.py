class AgentManager:

    def __init__(self):

        self.agents = {}

    def register(self, agent):

        self.agents[agent.name] = agent

    def get(self, name):

        return self.agents.get(name)

    def execute(self, name, usuario, mensagem):

        agent = self.get(name)

        if agent is None:

            return {
                "type": "error",
                "text": f"Agente '{name}' não encontrado."
            }

        return agent.execute(
            usuario,
            mensagem
        )


agent_manager = AgentManager()