"""
L.I.Z.A CONFIG
"""

import os


# ====================================================
# API KEYS
# ====================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
)

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)


# ====================================================
# PROVIDER
# ====================================================

# auto = tenta os providers disponíveis
# groq = somente Groq
# openai = somente OpenAI
# gemini = somente Gemini

AI_PROVIDER = "auto"
# ====================================================
# MODELOS — GROQ
# ====================================================

MODEL_GROQ_CHAT = (
    "llama-3.3-70b-versatile"
)

MODEL_GROQ_FAST = (
    "llama-3.1-8b-instant"
)

MODEL_GROQ_REASONING = (
    "llama-3.1-8b-instant"
)

MODEL_GROQ_VISION = (
    "meta-llama/llama-4-scout-17b-16e-instruct"
)


# ====================================================
# MODELOS — OPENAI
# ====================================================

MODEL_OPENAI_CHAT = "gpt-5"

MODEL_OPENAI_FAST = "gpt-5-mini"

MODEL_OPENAI_REASONING = "gpt-5"

MODEL_OPENAI_VISION = "gpt-5"


# ====================================================
# MODELOS — GEMINI
# ====================================================

MODEL_GEMINI_CHAT = (
    "gemini-3-flash-preview"
)

MODEL_GEMINI_FAST = (
    "gemini-3-flash-preview"
)

MODEL_GEMINI_REASONING = (
    "gemini-3-flash-preview"
)

MODEL_GEMINI_VISION = (
    "gemini-3-flash-preview"
)


# ====================================================
# SERVIDOR
# ====================================================

HOST = "0.0.0.0"

PORT = 5000

DEBUG = True


# ====================================================
# IA
# ====================================================

DEFAULT_LANGUAGE = "pt-BR"

DEFAULT_USER = "Beto"

TEMPERATURE_CHAT = 0.7

TEMPERATURE_REASONING = 0.2

MAX_TOKENS_CHAT = 4096

MAX_TOKENS_REASONING = 8192


# ====================================================
# MEMÓRIA
# ====================================================

ENABLE_MEMORY = True

MAX_MEMORY = 50

MEMORY_DATABASE = "liza.db"


# ====================================================
# VOZ
# ====================================================

VOICE_ENABLED = True

VOICE_LANGUAGE = "pt-BR"

VOICE_SPEED = 1.0

VOICE_PITCH = 1.0


# ====================================================
# ANDROID
# ====================================================

ANDROID_ENABLED = True

ALLOW_OPEN_APPS = True

ALLOW_CALLS = True

ALLOW_SMS = True

ALLOW_WHATSAPP = True

ALLOW_VOLUME = True


# ====================================================
# VISÃO
# ====================================================

VISION_ENABLED = True

MAX_IMAGE_SIZE = 10 * 1024 * 1024


# ====================================================
# LOGS
# ====================================================

ENABLE_LOGS = True

LOG_LEVEL = "INFO"


# ====================================================
# PLUGINS
# ====================================================

ENABLE_PLUGINS = True


# ====================================================
# SEGURANÇA
# ====================================================

ALLOW_REMOTE_COMMANDS = False

ALLOW_DANGEROUS_COMMANDS = False


# ====================================================
# PERSONALIDADE
# ====================================================

AI_NAME = "L.I.Z.A."

DEVELOPER = "Beto"

VERSION = "3.0"