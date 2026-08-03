"""
====================================================
L.I.Z.A Command
====================================================
"""

from dataclasses import dataclass, field


@dataclass
class Command:

    action: str

    parameters: dict = field(default_factory=dict)

    wait_result: bool = True

    timeout: int = 30