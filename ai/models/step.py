from dataclasses import dataclass, field


@dataclass
class Step:

    id: str

    action: str

    parameters: dict = field(default_factory=dict)

    status: str = "pending"

    retries: int = 0