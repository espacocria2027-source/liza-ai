from dataclasses import dataclass, field


@dataclass
class WorkflowStep:

    id: int

    agent: str

    action: str

    parameters: dict = field(default_factory=dict)

    wait_result: bool = True

    timeout: int = 30