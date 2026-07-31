"""
=========================================
Planner Models
=========================================
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Step:

    action: str

    parameters: Dict = field(default_factory=dict)


@dataclass
class Plan:

    steps: List[Step] = field(default_factory=list)

    message: str = ""
