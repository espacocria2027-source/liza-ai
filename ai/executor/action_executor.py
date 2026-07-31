"""
=========================================
Action Executor
=========================================
"""

from ai.executor.command import Command
from ai.executor.command_package import CommandPackage


class ActionExecutor:

    def execute(self, plan):

        pacote = CommandPackage()

        pacote.message = plan.message

        for step in plan.steps:

            pacote.commands.append(

                Command(

                    action=step.action,

                    parameters=step.parameters

                )

            )

        return pacote


executor = ActionExecutor()