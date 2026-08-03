"""
====================================================
L.I.Z.A Android Agent
====================================================
"""

from agents.base_agent import BaseAgent

from commands.command_factory import factory
from commands.execution import builder


class AndroidAgent(BaseAgent):

    @property
    def name(self):

        return "android"

    def execute(self, usuario, command):

        action = command.get(

            "action",

            "UNKNOWN"

        )

        parameters = command.get(

            "parameters",

            {}

        )

        message = command.get(

            "message",

            "Executando comando."

        )

        package = factory.create(

            action=action,

            parameters=parameters,

            message=message

        )

        execution = builder.build(

            package

        )

        return {

            "type": "execution",

            "execution_id": execution["execution_id"],

            "package": execution["package"]

        }