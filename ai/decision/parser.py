"""
=========================================
L.I.Z.A JSON Parser
=========================================
"""

import json


DEFAULT_RESPONSE = {
    "intent": "chat",
    "action": "",
    "parameters": {}
}


def parse(text: str) -> dict:
    """
    Converte a resposta da IA em um dicionário válido.
    """

    if not text:
        return DEFAULT_RESPONSE.copy()

    text = text.strip()

    # Remove markdown
    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:

        data = json.loads(text)

    except Exception:

        return DEFAULT_RESPONSE.copy()

    if not isinstance(data, dict):
        return DEFAULT_RESPONSE.copy()

    data.setdefault("intent", "chat")
    data.setdefault("action", "")
    data.setdefault("parameters", {})

    if not isinstance(data["parameters"], dict):
        data["parameters"] = {}

    return data