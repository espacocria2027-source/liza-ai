"""
====================================================
L.I.Z.A Commands
====================================================
"""

from dataclasses import dataclass, field


@dataclass
class CommandDefinition:

    name: str

    patterns: list[str]

    action: str


@dataclass
class Command:

    action: str

    parameters: dict = field(default_factory=dict)

    wait_result: bool = True

    timeout: int = 30