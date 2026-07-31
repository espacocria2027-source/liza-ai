"""
====================================================
FORMATADOR DA L.I.Z.A.
====================================================
"""

import re

# ====================================================
# LINGUAGENS SUPORTADAS
# ====================================================

LANGUAGES = [

    "python",
    "kotlin",
    "java",
    "javascript",
    "js",
    "typescript",
    "ts",
    "html",
    "css",
    "xml",
    "json",
    "sql",
    "php",
    "c",
    "cpp",
    "csharp",
    "go",
    "rust",
    "swift",
    "dart",
    "yaml",
    "bash",
    "shell"

]

# ====================================================
# REMOVE *TEXTO*
# ====================================================

def remove_asterisks(text: str) -> str:

    return re.sub(r"\*(.*?)\*", r"\1", text)

# ====================================================
# CONVERTE LISTAS PARA →
# ====================================================

def convert_lists(text: str) -> str:

    lines = []

    for line in text.split("\n"):

        stripped = line.strip()

        if stripped.startswith("- "):

            lines.append("→ " + stripped[2:])

        elif stripped.startswith("* "):

            lines.append("→ " + stripped[2:])

        elif stripped.startswith("• "):

            lines.append("→ " + stripped[2:])

        else:

            lines.append(line)

    return "\n".join(lines)

# ====================================================
# REMOVE ESPAÇOS DUPLOS
# ====================================================

def normalize_spaces(text: str) -> str:

    return re.sub(r"\n{3,}", "\n\n", text)

# ====================================================
# DETECTA BLOCO DE CÓDIGO
# ====================================================

def contains_code(text: str) -> bool:

    lower = text.lower()

    for language in LANGUAGES:

        if f"```{language}" in lower:

            return True

    return False

# ====================================================
# DETECTA A LINGUAGEM
# ====================================================

def detect_language(text: str):

    lower = text.lower()

    for language in LANGUAGES:

        if f"```{language}" in lower:

            return language

    return None

# ====================================================
# LIMPA O MARKDOWN
# ====================================================

def clean_markdown(text: str) -> str:

    text = remove_asterisks(text)

    text = convert_lists(text)

    text = normalize_spaces(text)

    return text.strip()

# ====================================================
# PREPARA A RESPOSTA
# ====================================================

def prepare_response(text: str):

    cleaned = clean_markdown(text)

    return {

        "message": cleaned,

        "hasCode": contains_code(cleaned),

        "language": detect_language(cleaned)

    }