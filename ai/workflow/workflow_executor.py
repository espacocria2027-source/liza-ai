from agents.agent_manager import agent_manager

from ai.workflow.workflow_result import WorkflowResult


class WorkflowExecutor:

    def execute(self, usuario, workflow):

        respostas = []

        for step in workflow.steps:

            resposta = agent_manager.execute(

                step.agent,

                usuario,

                {

                    "action": step.action,

                    "parameters": step.parameters

                }

            )

            respostas.append(resposta)

        return WorkflowResult(

            success=True,

            message=workflow.success_message,

            steps=respostas

        )


workflow_executor = WorkflowExecutor()