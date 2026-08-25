# ====================================================
# L.I.Z.A. — SOURCE SCORER
# ====================================================

from services.research.search_provider import SearchResult


class SourceScorer:

    def score(
        self,
        sources: list[SearchResult]
    ) -> list[SearchResult]:

        scored = []

        for source in sources:

            score = self._calculate_score(
                source
            )

            scored.append(
                (
                    score,
                    source
                )
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            source
            for _, source in scored
        ]


    # =================================================
    # SCORE FINAL
    # =================================================

    def _calculate_score(
        self,
        source: SearchResult
    ) -> float:

        provider_score = (
            source.provider_score
            if source.provider_score is not None
            else 0.5
        )

        authority_score = (
            self._authority_score(
                source.domain
            )
        )

        final_score = (
            provider_score * 0.60
            +
            authority_score * 0.40
        )

        return self._clamp(
            final_score
        )


    # =================================================
    # AUTORIDADE
    # =================================================

    def _authority_score(
        self,
        domain: str
    ) -> float:

        domain = (
            domain
            .lower()
            .removeprefix("www.")
        )


        # ---------------------------------------------
        # GOVERNO
        # ---------------------------------------------

        if (
            domain.endswith(".gov.br")
            or domain.endswith(".gov")
        ):
            return 1.0


        # ---------------------------------------------
        # ACADÊMICO
        # ---------------------------------------------

        if (
            domain.endswith(".edu.br")
            or domain.endswith(".edu")
        ):
            return 0.95


        # ---------------------------------------------
        # FONTES OFICIAIS
        # ---------------------------------------------

        official_domains = {

            "kotlinlang.org",

            "developer.android.com",

            "firebase.google.com",

            "developers.google.com",

            "docs.python.org",

            "python.org",

            "developer.mozilla.org",

            "developer.apple.com",

            "learn.microsoft.com",

            "docs.microsoft.com"

        }


        if domain in official_domains:
            return 0.95


        # ---------------------------------------------
        # GRANDES PLATAFORMAS TÉCNICAS
        # ---------------------------------------------

        major_domains = {

            "github.com",

            "stackoverflow.com",

            "wikipedia.org"

        }


        if domain in major_domains:
            return 0.80


        # ---------------------------------------------
        # COMUNIDADES
        # ---------------------------------------------

        community_domains = {

            "reddit.com",

            "stackexchange.com"

        }


        if domain in community_domains:
            return 0.55


        # ---------------------------------------------
        # DOMÍNIO DESCONHECIDO
        # ---------------------------------------------

        return 0.50


    # =================================================
    # NORMALIZAÇÃO
    # =================================================

    @staticmethod
    def _clamp(
        value: float
    ) -> float:

        return max(
            0.0,
            min(
                1.0,
                value
            )
        )