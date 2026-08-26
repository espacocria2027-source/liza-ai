class AgentManager:

    def __init__(self):

        self.agents = {}


    # ==================================================
    # REGISTRAR AGENTE
    # ==================================================

    def register(self, agent):

        self.agents[agent.name] = agent


    # ==================================================
    # OBTER AGENTE
    # ==================================================

    def get(self, name):

        return self.agents.get(name)


    # ==================================================
    # EXECUTAR AGENTE
    # ==================================================

    def execute(
        self,
        name,
        usuario,
        mensagem,
        prompt=""
    ):

        agent = self.get(name)


        # ==================================================
        # AGENTE NÃO ENCONTRADO
        # ==================================================

        if agent is None:

            return {

                "type":
                    "error",

                "text":
                    f"Agente '{name}' não encontrado."

            }


        # ==================================================
        # EXECUTAR
        # ==================================================

        return agent.execute(

            usuario,

            mensagem,

            prompt

        )


# ======================================================
# INSTÂNCIA GLOBAL
# ======================================================

agent_manager = AgentManager()