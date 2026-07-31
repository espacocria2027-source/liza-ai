from agents.base_agent import BaseAgent

from ai.planner.planner import planner
from ai.executor.action_executor import executor

from android.bridge import create_execution


class AndroidAgent(BaseAgent):

    @property
    def name(self):

        return "android"

    def execute(self, usuario, mensagem):

        plano = planner.create(mensagem)

        pacote = executor.execute(plano)

        execution = create_execution({

            "success": pacote.success,

            "message": pacote.message,

            "commands": [

                {

                    "action": cmd.action,

                    "parameters": cmd.parameters,

                    "wait_result": cmd.wait_result,

                    "timeout": cmd.timeout

                }

                for cmd in pacote.commands

            ]

        })

        return {

            "type": "execution",

            "execution_id": execution["execution_id"],

            "package": execution["package"]

        }