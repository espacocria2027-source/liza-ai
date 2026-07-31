"""
=========================================
L.I.Z.A Planner Engine V2
=========================================
"""

import json

from dataclasses import dataclass
from typing import List


@dataclass
class Step:

    action: str

    parameters: dict


@dataclass
class Plan:

    goal: str

    message: str

    steps: List[Step]


class PlannerEngine:

    def create(self, reasoning_output):

        if isinstance(reasoning_output, str):

            reasoning = json.loads(reasoning_output)

        else:

            reasoning = reasoning_output

        goal = reasoning.get("goal", "")

        intent = reasoning.get("intent", "chat")

        message = ""

        steps = []

        # ===========================
        # Abrir aplicativo
        # ===========================

        if goal.lower().startswith("abrir"):

            app = goal.replace("Abrir", "").strip()

            message = f"Abrindo {app}."

            steps.append(

                Step(

                    action="OPEN_APP",

                    parameters={

                        "app": app

                    }

                )

            )

        # ===========================
        # Pesquisa Google
        # ===========================

        elif intent == "search":

            query = reasoning.get("query", goal)

            message = "Pesquisando."

            steps.append(

                Step(

                    action="GOOGLE_SEARCH",

                    parameters={

                        "query": query

                    }

                )

            )

        # ===========================
        # Conversa
        # ===========================

        elif intent == "chat":

            message = "Respondendo."

        # ===========================
        # Ação Genérica
        # ===========================

        elif intent == "action":

            message = "Executando."

            steps.append(

                Step(

                    action=reasoning.get(

                        "action",

                        "UNKNOWN"

                    ),

                    parameters=reasoning.get(

                        "parameters",

                        {}

                    )

                )

            )

        return Plan(

            goal=goal,

            message=message,

            steps=steps

        )


planner_engine = PlannerEngine()