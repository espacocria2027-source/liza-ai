"""
=========================================
Decision Types
=========================================
"""

from enum import Enum


class Decision(str, Enum):

    CHAT = "chat"

    ACTION = "action"

    SEARCH = "search"

    AUTOMATION = "automation"

    UNKNOWN = "unknown"