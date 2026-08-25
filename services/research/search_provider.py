# ====================================================
# L.I.Z.A. — SEARCH PROVIDER
# ====================================================

from dataclasses import dataclass
from typing import List


@dataclass
class SearchResult:

    title: str

    url: str

    domain: str

    snippet: str = ""

    published_at: str | None = None

    # Score fornecido pelo mecanismo de pesquisa.
    # Não inventamos esse valor.
    provider_score: float | None = None


class SearchProvider:

    def search(
        self,
        query: str
    ) -> List[SearchResult]:

        raise NotImplementedError(
            "O provedor de pesquisa ainda não foi configurado."
        )