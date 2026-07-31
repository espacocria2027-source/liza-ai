"""
=========================================
L.I.Z.A CONFIG
=========================================
"""

import os

# API

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Modelos

MODEL_CHAT = "llama-3.3-70b-versatile"

MODEL_VISION = "meta-llama/llama-4-scout-17b-16e-instruct"

MODEL_FAST = "llama-3.1-8b-instant"

MODEL_REASONING = "openai/gpt-oss-120b"