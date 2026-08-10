from pathlib import Path

PROMPTS_DIR = Path("prompt")

def carregar_prompt(nome):

    caminho = PROMPTS_DIR / nome

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return arquivo.read()