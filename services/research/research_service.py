# ====================================================
# L.I.Z.A. — RESEARCH SERVICE
# ====================================================

from services.research.search_provider import (
    SearchProvider,
    SearchResult
)

from services.research.source_scorer import (
    SourceScorer
)

from services.research.answer_synthesizer import (
    AnswerSynthesizer
)

from services.research.evidence_analyzer import (
    EvidenceAnalyzer
)


class ResearchService:

    def __init__(
        self,
        search_provider: SearchProvider,
        source_scorer: SourceScorer,
        answer_synthesizer: AnswerSynthesizer,
        evidence_analyzer: EvidenceAnalyzer
    ):

        self.search_provider = (
            search_provider
        )

        self.source_scorer = (
            source_scorer
        )

        self.answer_synthesizer = (
            answer_synthesizer
        )

        self.evidence_analyzer = (
            evidence_analyzer
        )


    # =================================================
    # PESQUISA PRINCIPAL
    # =================================================

    def research(
        self,
        query: str,
        response_length: str = "medium"
    ):

        query = query.strip()

        if not query:

            raise ValueError(
                "A consulta não pode estar vazia."
            )


        # =============================================
        # NORMALIZAR TAMANHO DA RESPOSTA
        # =============================================

        if response_length not in {
            "short",
            "medium",
            "long"
        }:

            response_length = "medium"


        # =============================================
        # 1. BUSCAR NA WEB
        # =============================================

        results = (
            self.search_provider.search(
                query
            )
        )


        # =============================================
        # 2. LIMPAR RESULTADOS
        # =============================================

        results = (
            self._clean_results(
                results
            )
        )


        # =============================================
        # NENHUMA FONTE
        # =============================================

        if not results:

            return {

                "query":
                    query,

                "answer":
                    (
                        "Não encontrei fontes "
                        "suficientes para responder "
                        "com segurança."
                    ),

                "searchedAutomatically":
                    True,

                "confidence":
                    0.0,

                "hasConflict":
                    False,

                "conflictType":
                    None,

                "evidenceReason":
                    (
                        "Nenhuma fonte válida "
                        "foi encontrada."
                    ),

                "sources":
                    [],

                "responseLength":
                    response_length

            }


        # =============================================
        # 3. CALCULAR PONTUAÇÃO
        # =============================================

        results = (
            self.source_scorer.score(
                results
            )
        )


        # =============================================
        # 4. SELECIONAR FONTES
        # =============================================

        results = (
            self._select_sources(
                results
            )
        )


        # =============================================
        # 5. ANALISAR EVIDÊNCIAS
        # =============================================

        evidence = (
            self.evidence_analyzer.analyze(
                query,
                results
            )
        )


        # =============================================
        # 6. GERAR RESPOSTA
        # =============================================

        answer = (
            self.answer_synthesizer.synthesize(

                query,

                results,

                evidence,

                response_length
            )
        )


        # =============================================
        # 7. MONTAR FONTES
        # =============================================

        source_data = []


        for index, result in enumerate(
            results,
            start=1
        ):

            source_data.append({

                "index":
                    index,

                "title":
                    result.title,

                "url":
                    result.url,

                "domain":
                    result.domain,

                "snippet":
                    result.snippet,

                "publishedAt":
                    result.published_at,

                "providerScore":
                    result.provider_score

            })


        # =============================================
        # 8. RESULTADO FINAL
        # =============================================

        return {

            "query":
                query,

            "answer":
                answer,

            "searchedAutomatically":
                True,

            "confidence":
                evidence.confidence,

            "hasConflict":
                evidence.has_conflict,

            "conflictType":
                evidence.conflict_type,

            "evidenceReason":
                evidence.reason,

            "sources":
                source_data,

            "responseLength":
                response_length

        }


    # =================================================
    # LIMPEZA DOS RESULTADOS
    # =================================================

    def _clean_results(
        self,
        results: list[SearchResult]
    ) -> list[SearchResult]:

        cleaned = []

        seen_urls = set()


        for result in results:

            # -----------------------------------------
            # TÍTULO
            # -----------------------------------------

            if not result.title:

                continue


            # -----------------------------------------
            # URL
            # -----------------------------------------

            if not result.url:

                continue


            # -----------------------------------------
            # DOMÍNIO
            # -----------------------------------------

            if not result.domain:

                continue


            # -----------------------------------------
            # NORMALIZAR URL
            # -----------------------------------------

            normalized_url = (
                result.url
                .strip()
                .lower()
            )


            # -----------------------------------------
            # REMOVER DUPLICADAS
            # -----------------------------------------

            if (
                normalized_url
                in seen_urls
            ):

                continue


            seen_urls.add(
                normalized_url
            )


            cleaned.append(
                result
            )


        return cleaned


    # =================================================
    # SELEÇÃO INTELIGENTE
    # =================================================

    def _select_sources(
        self,
        sources: list[SearchResult]
    ) -> list[SearchResult]:

        selected = []

        domains_used = set()


        # =============================================
        # PRIMEIRA PASSAGEM
        #
        # Um resultado por domínio.
        # Isso aumenta a diversidade.
        # =============================================

        for source in sources:

            domain = (
                source.domain
                .lower()
                .removeprefix(
                    "www."
                )
            )


            if domain in domains_used:

                continue


            selected.append(
                source
            )

            domains_used.add(
                domain
            )


            if len(selected) >= 6:

                break


        # =============================================
        # SEGUNDA PASSAGEM
        #
        # Se não houver seis domínios diferentes,
        # usamos os melhores resultados restantes.
        # =============================================

        if len(selected) < 6:

            selected_urls = {

                source.url

                for source
                in selected

            }


            for source in sources:

                if source.url in selected_urls:

                    continue


                selected.append(
                    source
                )


                if len(selected) >= 6:

                    break


        return selected