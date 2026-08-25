# ====================================================
# L.I.Z.A. — TAVILY SEARCH PROVIDER
# ====================================================

import os

from typing import List
from urllib.parse import urlparse

from tavily import TavilyClient

from services.research.search_provider import (
    SearchProvider,
    SearchResult
)


class TavilySearchProvider(SearchProvider):

    # =================================================
    # INICIALIZAÇÃO
    # =================================================

    def __init__(
        self,
        api_key: str | None = None
    ):

        self.api_key = (
            api_key
            or os.getenv(
                "TAVILY_API_KEY"
            )
        )

        if not self.api_key:

            raise RuntimeError(
                "TAVILY_API_KEY não configurada."
            )

        self.client = TavilyClient(
            api_key=self.api_key
        )


    # =================================================
    # PESQUISA
    # =================================================

    def search(
        self,
        query: str
    ) -> List[SearchResult]:

        query = query.strip()

        if not query:

            raise ValueError(
                "A consulta não pode estar vazia."
            )


        response = self.client.search(

            query=query,

            search_depth="basic",

            topic="general",

            max_results=10,

            include_answer=False,

            include_raw_content=False

        )


        results: List[SearchResult] = []


        for item in response.get(
            "results",
            []
        ):

            title = (
                item.get(
                    "title",
                    ""
                )
                .strip()
            )

            url = (
                item.get(
                    "url",
                    ""
                )
                .strip()
            )

            content = (
                item.get(
                    "content",
                    ""
                )
                .strip()
            )

            provider_score = (
                item.get(
                    "score"
                )
            )


            if not title or not url:

                continue


            domain = (
                self._extract_domain(
                    url
                )
            )


            results.append(

                SearchResult(

                    title=title,

                    url=url,

                    domain=domain,

                    snippet=content,

                    published_at=None,

                    provider_score=(
                        self._safe_score(
                            provider_score
                        )
                    )

                )

            )


        return results


    # =================================================
    # SCORE
    # =================================================

    @staticmethod
    def _safe_score(
        value
    ) -> float | None:

        if value is None:

            return None

        try:

            score = float(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return None


        return max(
            0.0,
            min(
                1.0,
                score
            )
        )


    # =================================================
    # DOMÍNIO
    # =================================================

    @staticmethod
    def _extract_domain(
        url: str
    ) -> str:

        try:

            parsed = urlparse(
                url
            )

            domain = (
                parsed.netloc
                .lower()
                .removeprefix(
                    "www."
                )
            )

            return domain

        except Exception:

            return ""