"""
=========================================
Learning Service
=========================================
"""

import json
from pathlib import Path

from ai.learning.extractor import extract


ARQUIVO = Path("ai/learning/facts.json")


class LearningService:

    def __init__(self):

        if not ARQUIVO.exists():

            ARQUIVO.write_text(
                "{}",
                encoding="utf-8"
            )

    def _load(self):

        with open(
            ARQUIVO,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def _save(self, dados):

        with open(
            ARQUIVO,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                dados,
                f,
                ensure_ascii=False,
                indent=4
            )

    def learn(self, usuario, mensagem):

        banco = self._load()

        if usuario not in banco:

            banco[usuario] = []

        fatos = extract(mensagem)

        existentes = {

            (
                f["type"],
                f["value"]
            )

            for f in banco[usuario]

        }

        for fato in fatos:

            chave = (

                fato["type"],

                fato["value"]

            )

            if chave not in existentes:

                banco[usuario].append(fato)

        self._save(banco)

    def get_facts(self, usuario):

        banco = self._load()

        return banco.get(usuario, [])


learning = LearningService()