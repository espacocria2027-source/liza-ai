"""
====================================================
Workflow Parser
====================================================
"""

import json

from ai.workflow.workflow import Workflow
from ai.workflow.step import WorkflowStep


class WorkflowParser:

    def parse(self, text):

        workflow = Workflow(name="Workflow")

        try:

            data = json.loads(text)

        except Exception:

            return workflow

        workflow.name = data.get(

            "name",

            "Workflow"

        )

        workflow.success_message = data.get(

            "success_message",

            "Concluído."

        )

        workflow.failure_message = data.get(

            "failure_message",

            "Falhou."

        )

        for index, step in enumerate(

            data.get("steps", []),

            start=1

        ):

            workflow.add_step(

                WorkflowStep(

                    id=index,

                    agent=step.get(

                        "agent",

                        "chat"

                    ),

                    action=step.get(

                        "action",

                        ""

                    ),

                    parameters=step.get(

                        "parameters",

                        {}

                    )

                )

            )

        return workflow


workflow_parser = WorkflowParser()