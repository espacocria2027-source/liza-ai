"""
====================================================
L.I.Z.A Command Factory
====================================================
"""

from commands.command import Command
from commands.command_package import CommandPackage


class CommandFactory:

    def create(
        self,
        action,
        parameters=None,
        message="Executando comando."
    ):

        package = CommandPackage()

        package.success = True
        package.message = message

        package.commands.append(

            Command(

                action=action,
                parameters=parameters or {},
                wait_result=True,
                timeout=30

            )

        )

        return package


factory = CommandFactory()