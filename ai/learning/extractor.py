"""
=========================================
L.I.Z.A Fact Extractor
=========================================
"""

import re


PATTERNS = [

    (
        r"meu projeto (?:é|se chama) (.+)",
        "project"
    ),

    (
        r"estou desenvolvendo (.+)",
        "project"
    ),

    (
        r"uso (.+)",
        "technology"
    ),

    (
        r"programo em (.+)",
        "language"
    ),

    (
        r"quero aprender (.+)",
        "goal"
    )

]


def extract(texto):

    facts = []

    texto = texto.lower()

    for pattern, tipo in PATTERNS:

        resultado = re.search(pattern, texto)

        if resultado:

            facts.append({

                "type": tipo,

                "value": resultado.group(1).strip()

            })

    return facts