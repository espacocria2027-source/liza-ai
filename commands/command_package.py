"""
====================================================
L.I.Z.A Command Package
====================================================
"""

from dataclasses import dataclass, field

from commands.command import Command


@dataclass
class CommandPackage:

    success: bool = True

    message: str = ""

    commands: list[Command] = field(default_factory=list)