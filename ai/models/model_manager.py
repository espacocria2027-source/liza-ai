"""
L.I.Z.A. MODEL MANAGER
"""

from config import (
    MODEL_GROQ_CHAT,
    MODEL_GROQ_VISION,
    MODEL_GROQ_FAST,
    MODEL_GROQ_REASONING,

    MODEL_OPENAI_CHAT,
    MODEL_OPENAI_VISION,
    MODEL_OPENAI_FAST,
    MODEL_OPENAI_REASONING,

    MODEL_GEMINI_CHAT,
    MODEL_GEMINI_VISION,
    MODEL_GEMINI_FAST,
    MODEL_GEMINI_REASONING
)


class ModelManager:

    # ==================================================
    # GROQ
    # ==================================================

    @property
    def groq_chat(self):
        return MODEL_GROQ_CHAT

    @property
    def groq_vision(self):
        return MODEL_GROQ_VISION

    @property
    def groq_fast(self):
        return MODEL_GROQ_FAST

    @property
    def groq_reasoning(self):
        return MODEL_GROQ_REASONING

    # ==================================================
    # OPENAI
    # ==================================================

    @property
    def openai_chat(self):
        return MODEL_OPENAI_CHAT

    @property
    def openai_vision(self):
        return MODEL_OPENAI_VISION

    @property
    def openai_fast(self):
        return MODEL_OPENAI_FAST

    @property
    def openai_reasoning(self):
        return MODEL_OPENAI_REASONING

    # ==================================================
    # GEMINI
    # ==================================================

    @property
    def gemini_chat(self):
        return MODEL_GEMINI_CHAT

    @property
    def gemini_vision(self):
        return MODEL_GEMINI_VISION

    @property
    def gemini_fast(self):
        return MODEL_GEMINI_FAST

    @property
    def gemini_reasoning(self):
        return MODEL_GEMINI_REASONING


models = ModelManager()