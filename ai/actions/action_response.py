"""
=========================================
ACTION RESPONSE
=========================================
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ActionResponse:

    success: bool = True

    action: str = "chat"

    message: str = ""

    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):

        return {

            "success": self.success,

            "action": self.action,

            "message": self.message,

            "data": self.data

        }