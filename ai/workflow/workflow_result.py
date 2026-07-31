from dataclasses import dataclass, field


@dataclass
class WorkflowResult:

    success: bool

    message: str

    steps: list = field(default_factory=list)