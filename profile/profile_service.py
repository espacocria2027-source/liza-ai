"""
=========================================
L.I.Z.A Profile Service
=========================================
"""

import json
from pathlib import Path


ARQUIVO = Path("ai/profile/profiles.json")


class ProfileService:

    def __init__(self):

        if not ARQUIVO.exists():

            ARQUIVO.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with open(
                ARQUIVO,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump({}, f)

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
                indent=4,
                ensure_ascii=False
            )

    def get(self, usuario):

        dados = self._load()

        if usuario not in dados:

            dados[usuario] = {

                "likes_examples": True,

                "likes_complete_code": True,

                "likes_step_by_step": True,

                "short_answers": False,

                "preferred_language": "pt-BR"

            }

            self._save(dados)

        return dados[usuario]

    def update(self, usuario, **kwargs):

        dados = self._load()

        perfil = self.get(usuario)

        perfil.update(kwargs)

        dados[usuario] = perfil

        self._save(dados)


profile = ProfileService()