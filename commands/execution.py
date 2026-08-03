"""
====================================================
Execution Builder
====================================================
"""

from android.bridge import create_execution


class ExecutionBuilder:

    def build(self, package):

        return create_execution({

            "success": package.success,

            "message": package.message,

            "commands": [

                {

                    "action": cmd.action,

                    "parameters": cmd.parameters,

                    "wait_result": cmd.wait_result,

                    "timeout": cmd.timeout

                }

                for cmd in package.commands

            ]

        })


builder = ExecutionBuilder()