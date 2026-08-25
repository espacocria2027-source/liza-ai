# ====================================================
# L.I.Z.A. — EVIDENCE ANALYZER
# ====================================================

from dataclasses import dataclass
import re

from services.research.search_provider import SearchResult


@dataclass
class EvidenceAnalysis:

    confidence: float

    has_conflict: bool

    preferred_sources: list[int]

    reason: str

    conflict_type: str | None


class EvidenceAnalyzer:

    # =================================================
    # ANALISAR
    # =================================================

    def analyze(
        self,
        query: str,
        sources: list[SearchResult]
    ) -> EvidenceAnalysis:

        if not sources:

            return EvidenceAnalysis(

                confidence=0.0,

                has_conflict=False,

                preferred_sources=[],

                reason=(
                    "Nenhuma fonte válida "
                    "foi encontrada."
                ),

                conflict_type=None

            )


        # =============================================
        # RANKING
        # =============================================

        ranked = self._rank_sources(
            sources
        )


        preferred_sources = [

            index

            for index, _score
            in ranked[:3]

        ]


        # =============================================
        # DETECÇÃO DE CONFLITO
        # =============================================

        conflict_type = (
            self._detect_conflict_type(
                sources,
                query
            )
        )


        has_conflict = (
            conflict_type is not None
        )


        # =============================================
        # CONFIANÇA
        # =============================================

        confidence = (
            self._calculate_confidence(
                sources,
                ranked,
                has_conflict
            )
        )


        # =============================================
        # JUSTIFICATIVA
        # =============================================

        reason = (
            self._build_reason(
                sources,
                conflict_type
            )
        )


        return EvidenceAnalysis(

            confidence=confidence,

            has_conflict=has_conflict,

            preferred_sources=(
                preferred_sources
            ),

            reason=reason,

            conflict_type=(
                conflict_type
            )

        )


    # =================================================
    # RANKING
    # =================================================

    def _rank_sources(
        self,
        sources: list[SearchResult]
    ):

        ranked = []


        for index, source in enumerate(
            sources,
            start=1
        ):

            authority = (
                self._authority(
                    source.domain
                )
            )


            provider_score = (

                source.provider_score

                if source.provider_score
                is not None

                else 0.5

            )


            score = (

                authority * 0.60

                +

                provider_score * 0.40

            )


            ranked.append(

                (
                    index,
                    score
                )

            )


        ranked.sort(

            key=lambda item: item[1],

            reverse=True

        )


        return ranked


    # =================================================
    # AUTORIDADE
    # =================================================

    def _authority(
        self,
        domain: str
    ) -> float:

        domain = (
            domain
            .lower()
            .removeprefix(
                "www."
            )
        )


        # ---------------------------------------------
        # GOVERNO
        # ---------------------------------------------

        if (

            domain.endswith(
                ".gov.br"
            )

            or

            domain.endswith(
                ".gov"
            )

        ):

            return 1.0


        # ---------------------------------------------
        # ACADÊMICO
        # ---------------------------------------------

        if (

            domain.endswith(
                ".edu.br"
            )

            or

            domain.endswith(
                ".edu"
            )

        ):

            return 0.95


        # ---------------------------------------------
        # OFICIAIS
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

            "learn.microsoft.com"

        }


        if domain in official_domains:

            return 0.95


        # ---------------------------------------------
        # GRANDES PLATAFORMAS
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


        return 0.50


    # =================================================
    # CONFIANÇA
    # =================================================

    def _calculate_confidence(
        self,
        sources: list[SearchResult],
        ranked,
        has_conflict: bool
    ) -> float:

        if not ranked:

            return 0.0


        top_score = ranked[0][1]


        source_count_factor = min(

            len(sources) / 4.0,

            1.0

        )


        confidence = (

            top_score * 0.70

            +

            source_count_factor * 0.30

        )


        # ---------------------------------------------
        # PENALIDADE POR CONFLITO
        # ---------------------------------------------

        if has_conflict:

            confidence *= 0.75


        return max(

            0.0,

            min(

                1.0,

                confidence

            )

        )


    # =================================================
    # TIPO DE CONFLITO
    # =================================================

    def _detect_conflict_type(
        self,
        sources: list[SearchResult],
        query: str
    ) -> str | None:

        text = " ".join(

            (

                source.title
                + " "
                + source.snippet

            ).lower()

            for source in sources

        )


        # ---------------------------------------------
        # VERSÃO
        # ---------------------------------------------

        versions = set(

            self._extract_versions(
                text
            )

        )


        if len(versions) > 1:

            return "VERSION"


        # ---------------------------------------------
        # DATA
        # ---------------------------------------------

        dates = set(

            self._extract_dates(
                text
            )

        )


        if len(dates) > 1:

            return "DATE"


        # ---------------------------------------------
        # NÚMEROS
        # ---------------------------------------------

        if self._looks_like_numeric_question(
            query
        ):

            numbers = set(

                self._extract_numbers(
                    text
                )

            )


            if len(numbers) >= 2:

                return "NUMERIC"


        return None


    # =================================================
    # VERSÕES
    # =================================================

    @staticmethod
    def _extract_versions(
        text: str
    ) -> list[str]:

        matches = re.findall(

            r"\b\d+\.\d+"
            r"(?:\.\d+)?"
            r"(?:-[a-z0-9.]+)?\b",

            text

        )


        return list(

            dict.fromkeys(
                matches
            )

        )


    # =================================================
    # DATAS
    # =================================================

    @staticmethod
    def _extract_dates(
        text: str
    ) -> list[str]:

        patterns = [

            r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",

            r"\b\d{4}-\d{2}-\d{2}\b",

            r"\b(?:jan|fev|mar|abr|mai|jun|jul|ago|"
            r"set|out|nov|dez)[a-z]*\s+\d{4}\b"

        ]


        dates = []


        for pattern in patterns:

            dates.extend(

                re.findall(
                    pattern,
                    text,
                    flags=re.IGNORECASE
                )

            )


        return list(

            dict.fromkeys(
                dates
            )

        )


    # =================================================
    # NÚMEROS
    # =================================================

    @staticmethod
    def _extract_numbers(
        text: str
    ) -> list[str]:

        matches = re.findall(

            r"\b\d+(?:[.,]\d+)?\b",

            text

        )


        return list(

            dict.fromkeys(
                matches
            )

        )


    # =================================================
    # PERGUNTA NUMÉRICA
    # =================================================

    @staticmethod
    def _looks_like_numeric_question(
        query: str
    ) -> bool:

        keywords = (

            "quanto",

            "quantos",

            "quantas",

            "número",

            "numero",

            "porcentagem",

            "percentual",

            "população",

            "populacao",

            "preço",

            "preco",

            "valor",

            "idade",

            "altura",

            "distância",

            "distancia"

        )


        query = query.lower()


        return any(

            keyword in query

            for keyword in keywords

        )


    # =================================================
    # JUSTIFICATIVA
    # =================================================

    def _build_reason(
        self,
        sources: list[SearchResult],
        conflict_type: str | None
    ) -> str:

        if conflict_type == "VERSION":

            return (

                "As fontes apresentam versões "
                "diferentes. A L.I.Z.A. deve "
                "considerar a autoridade e a "
                "atualidade de cada fonte."

            )


        if conflict_type == "DATE":

            return (

                "As fontes apresentam datas "
                "diferentes. A L.I.Z.A. deve "
                "considerar o contexto e a "
                "data mais relevante."

            )


        if conflict_type == "NUMERIC":

            return (

                "As fontes apresentam valores "
                "numéricos diferentes. A L.I.Z.A. "
                "deve verificar o contexto de "
                "cada valor antes de responder."

            )


        return (

            "As fontes selecionadas não "
            "apresentaram sinais claros de "
            "conflito."

        )