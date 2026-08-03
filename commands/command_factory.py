"""
====================================================
Command Factory
====================================================
"""

from core.commands.command import Command
from core.commands.command_package import CommandPackage


class CommandFactory:

    def create(

        self,

        action,

        parameters=None,

        message="Executando comando."

    ):

        package = CommandPackage()

        package.message = message

        package.commands.append(

            Command(

                action=action,

                parameters=parameters or {}

            )

        )

        return package


factory = CommandFactory()