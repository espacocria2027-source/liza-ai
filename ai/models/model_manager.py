"""
=========================================
MODEL MANAGER
=========================================
"""

from config import (
    MODEL_CHAT,
    MODEL_VISION,
    MODEL_FAST,
    MODEL_REASONING
)


class ModelManager:

    @property
    def chat(self):
        return MODEL_CHAT

    @property
    def vision(self):
        return MODEL_VISION

    @property
    def fast(self):
        return MODEL_FAST

    @property
    def reasoning(self):
        return MODEL_REASONING


models = ModelManager()