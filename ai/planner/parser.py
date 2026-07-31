"""
=========================================
Planner Parser
=========================================
"""

import json

from ai.planner.models import Plan
from ai.planner.models import Step


def parse(text):

    try:

        data = json.loads(text)

    except Exception:

        return Plan()

    plano = Plan()

    plano.message = data.get("message", "")

    for item in data.get("steps", []):

        plano.steps.append(

            Step(

                action=item.get("action", ""),

                parameters=item.get(

                    "parameters",

                    {}

                )

            )

        )

    return plano