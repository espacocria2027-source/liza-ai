"""
=========================================
PLANO DE EXECUÇÃO
=========================================
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class Step:

    action: str

    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Plan:

    message: str = ""

    steps: List[Step] = field(default_factory=list)

    success: bool = True

    def to_dict(self):

        return {

            "success": self.success,

            "message": self.message,

            "steps":[

                {

                    "action": step.action,

                    "data": step.data

                }

                for step in self.steps

            ]

        }