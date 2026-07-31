"""
=========================================
Command Package
=========================================
"""

from dataclasses import dataclass, field

from ai.executor.command import Command


@dataclass
class CommandPackage:

    success: bool = True

    message: str = ""

    commands: list[Command] = field(default_factory=list)