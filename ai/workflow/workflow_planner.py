"""
====================================================
AI Workflow Planner
====================================================
"""

from ai.providers.model_provider import provider

from ai.workflow.workflow_parser import workflow_parser


SYSTEM_PROMPT = """
Você é o planejador da L.I.Z.A.

Nunca converse.

Nunca explique.

Sua única função é gerar workflows.

Responda SOMENTE JSON.

Formato:

{

    "name":"",

    "success_message":"",

    "failure_message":"",

    "steps":[

        {

            "agent":"",

            "action":"",

            "parameters":{}

        }

    ]

}

Agentes disponíveis:

chat

android

spotify

gmail

calendar

vision

programmer

automation

search
"""


class AIWorkflowPlanner:

    def create(self, mensagem):

        resposta = provider.reasoning(

            [

                {

                    "role":"system",

                    "content":SYSTEM_PROMPT

                },

                {

                    "role":"user",

                    "content":mensagem

                }

            ]

        )

        return workflow_parser.parse(

            resposta

        )


ai_workflow_planner = AIWorkflowPlanner()