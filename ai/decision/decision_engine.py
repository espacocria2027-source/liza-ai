"""
====================================================
L.I.Z.A Decision Engine
====================================================
"""

import detectors.registry

from detectors.detector_manager import detector_manager
from agents.agent_manager import agent_manager

from services.research.research_service import (
    ResearchService
)

from services.research.tavily_search_provider import (
    TavilySearchProvider
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


class DecisionEngine:

    def __init__(self):

        # ==================================================
        # PESQUISA WEB
        # ==================================================

        self.research_service = ResearchService(

            TavilySearchProvider(),

            SourceScorer(),

            AnswerSynthesizer(),

            EvidenceAnalyzer()

        )


    def process(
        self,
        usuario,
        mensagem
    ):

        # ================================================
        # DETECTORES
        # ================================================

        resultado = detector_manager.detect(

            mensagem

        )


        intent = resultado.get(

            "intent",

            "chat"

        )


        # ================================================
        # ANDROID
        # ================================================

        if intent == "android":

            return agent_manager.execute(

                "android",

                usuario,

                resultado

            )


        # ================================================
        # PROGRAMADOR
        # ================================================

        if intent == "programmer":

            return agent_manager.execute(

                "programmer",

                usuario,

                mensagem

            )


        # ================================================
        # PESQUISA WEB
        # ================================================

        if intent == "research":

            query = resultado.get(

                "query",

                mensagem

            )


            try:

                pesquisa = (
                    self.research_service.research(
                        query
                    )
                )


                return {

                    "type":
                        "research",

                    "text":
                        pesquisa.get(
                            "answer",
                            ""
                        ),

                    "query":
                        pesquisa.get(
                            "query",
                            query
                        ),

                    "searchedAutomatically":
                        pesquisa.get(
                            "searchedAutomatically",
                            True
                        ),

                    "confidence":
                        pesquisa.get(
                            "confidence",
                            0.0
                        ),

                    "hasConflict":
                        pesquisa.get(
                            "hasConflict",
                            False
                        ),

                    "conflictType":
                        pesquisa.get(
                            "conflictType",
                            None
                        ),

                    "evidenceReason":
                        pesquisa.get(
                            "evidenceReason",
                            ""
                        ),

                    "sources":
                        pesquisa.get(
                            "sources",
                            []
                        )

                }


            except Exception as error:

                print(
                    "❌ Erro na pesquisa automática:",
                    error
                )


                # ========================================
                # FALLBACK
                # ========================================

                return agent_manager.execute(

                    "chat",

                    usuario,

                    mensagem

                )


        # ================================================
        # CHAT
        # ================================================

        return agent_manager.execute(

            "chat",

            usuario,

            mensagem

        )


decision_engine = DecisionEngine()