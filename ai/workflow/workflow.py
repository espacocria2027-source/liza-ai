from dataclasses import dataclass, field

from ai.workflow.step import WorkflowStep


@dataclass
class Workflow:

    name: str

    steps: list[WorkflowStep] = field(default_factory=list)

    success_message: str = ""

    failure_message: str = ""

    def add_step(self, step):

        self.steps.append(step)