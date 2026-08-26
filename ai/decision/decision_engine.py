"""
====================================================
L.I.Z.A. Decision Engine
====================================================
"""

import re

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


    # =====================================================
    # PESQUISA SOLICITADA PELO USUÁRIO
    # =====================================================

    def _user_requested_research(
        self,
        mensagem
    ):

        texto = (
            mensagem
            .strip()
            .lower()
        )


        # =================================================
        # COMANDOS EXPLÍCITOS
        # =================================================

        explicit_research = [

            "faça uma pesquisa",
            "faca uma pesquisa",

            "faça uma busca",
            "faca uma busca",

            "faça uma busca na internet",
            "faca uma busca na internet",

            "faça uma pesquisa na internet",
            "faca uma pesquisa na internet",

            "faça uma pesquisa na web",
            "faca uma pesquisa na web",

            "fazer uma pesquisa",
            "fazer uma busca",

            "pesquise na internet",
            "pesquise na web",

            "pesquisa na internet",
            "pesquisa na web",

            "procure na internet",
            "procure na web",

            "procura na internet",
            "procura na web",

            "busque na internet",
            "busque na web",

            "busca na internet",
            "busca na web",

            "verifique na internet",
            "verifique na web",

            "confira na internet",
            "confira na web",

            "pesquise isso",
            "pesquisa isso",

            "procure isso",
            "procura isso",

            "busque isso",
            "busca isso"

        ]


        if any(
            termo in texto
            for termo in explicit_research
        ):

            return True


        # =================================================
        # COMANDO CURTO
        #
        # "Liza, pesquise sobre Kotlin"
        # =================================================

        command_patterns = [

            r"^(?:liza[,\s]+)?pesquise\b",
            r"^(?:liza[,\s]+)?pesquisa\b",
            r"^(?:liza[,\s]+)?pesquisar\b",

            r"^(?:liza[,\s]+)?procure\b",
            r"^(?:liza[,\s]+)?procura\b",

            r"^(?:liza[,\s]+)?busque\b",
            r"^(?:liza[,\s]+)?busca\b",

            r"^(?:liza[,\s]+)?verifique\b",
            r"^(?:liza[,\s]+)?confira\b"

        ]


        for pattern in command_patterns:

            if re.match(
                pattern,
                texto
            ):

                return True


        return False


    # =====================================================
    # NECESSIDADE DE PESQUISA AUTOMÁTICA
    # =====================================================

    def _needs_automatic_research(
        self,
        mensagem,
        resultado
    ):

        texto = (
            mensagem
            .strip()
            .lower()
        )


        # =================================================
        # INFORMAÇÕES QUE MUDAM COM O TEMPO
        # =================================================

        current_terms = [

            "atual",
            "atualmente",

            "mais recente",
            "mais recentes",

            "última versão",
            "ultima versão",
            "ultima versao",

            "última atualização",
            "ultima atualização",
            "ultima atualizacao",

            "versão atual",
            "versao atual",

            "versão mais recente",
            "versao mais recente",

            "hoje",
            "agora",

            "neste momento",
            "no momento",

            "recentemente",

            "últimas notícias",
            "ultimas noticias",

            "últimas novidades",
            "ultimas novidades",

            "notícias recentes",
            "noticias recentes",

            "notícia recente",
            "noticia recente",

            "lançamento recente",
            "lancamento recente",

            "lançamentos recentes",
            "lancamentos recentes",

            "release atual",
            "release mais recente"

        ]


        if any(
            termo in texto
            for termo in current_terms
        ):

            return True


        # =================================================
        # NOTÍCIAS
        # =================================================

        news_terms = [

            "notícia",
            "noticia",

            "notícias",
            "noticias",

            "breaking news",

            "o que aconteceu hoje",

            "o que aconteceu recentemente"

        ]


        if any(
            termo in texto
            for termo in news_terms
        ):

            return True


        # =================================================
        # PREÇOS / COTAÇÕES
        # =================================================

        price_terms = [

            "preço atual",
            "preco atual",

            "preço hoje",
            "preco hoje",

            "quanto custa hoje",

            "valor atual",

            "cotação",
            "cotacao",

            "dólar hoje",
            "dolar hoje",

            "euro hoje",

            "bitcoin hoje",

            "ações hoje",
            "acoes hoje"

        ]


        if any(
            termo in texto
            for termo in price_terms
        ):

            return True


        # =================================================
        # CLIMA / TEMPO
        # =================================================

        weather_terms = [

            "clima agora",
            "clima hoje",

            "tempo agora",
            "tempo hoje",

            "vai chover hoje",
            "vai chover",

            "previsão do tempo",
            "previsao do tempo"

        ]


        if any(
            termo in texto
            for termo in weather_terms
        ):

            return True


        # =================================================
        # EVENTOS / DISPONIBILIDADE
        # =================================================

        availability_terms = [

            "está disponível",
            "esta disponivel",

            "ainda está disponível",
            "ainda esta disponivel",

            "quando vai lançar",
            "quando vai lancar",

            "quando será lançado",
            "quando sera lancado",

            "data de lançamento",
            "data de lancamento"

        ]


        if any(
            termo in texto
            for termo in availability_terms
        ):

            return True


        # =================================================
        # PROGRAMADOR
        #
        # Programação sozinha NÃO ativa Tavily.
        # =================================================

        if resultado.get(
            "intent"
        ) == "programmer":

            documentation_terms = [

                "documentação atual",
                "documentacao atual",

                "documentação oficial",
                "documentacao oficial",

                "docs atuais",

                "documentação mais recente",
                "documentacao mais recente",

                "api atual",
                "api mais recente",

                "mudou na versão",
                "mudou na versao",

                "mudanças da versão",
                "mudancas da versao",

                "release",

                "changelog",

                "breaking changes"

            ]


            if any(
                termo in texto
                for termo in documentation_terms
            ):

                return True


            return False


        # =================================================
        # CHAT NORMAL
        # =================================================

        return False


    # =====================================================
    # DECISÃO FINAL DE PESQUISA
    # =====================================================

    def _needs_research(
        self,
        mensagem,
        resultado
    ):

        # =================================================
        # PESQUISA MANUAL
        #
        # Se o usuário pediu explicitamente,
        # NÃO importa se o assunto é simples.
        # =================================================

        if self._user_requested_research(
            mensagem
        ):

            return True


        # =================================================
        # PESQUISA AUTOMÁTICA
        # =================================================

        return self._needs_automatic_research(

            mensagem,

            resultado

        )


    # =====================================================
    # TAMANHO DA RESPOSTA
    # =====================================================

    def _response_length(
        self,
        mensagem
    ):

        texto = (
            mensagem
            .strip()
            .lower()
        )


        # =================================================
        # RESPOSTA CURTA
        # =================================================

        short_terms = [

            "resuma",
            "resumido",
            "resumida",

            "bem curto",
            "bem curta",

            "curto",
            "curta",

            "em poucas palavras",

            "resposta rápida",
            "resposta rapida",

            "só a resposta",
            "so a resposta",

            "direto ao ponto",

            "seja breve",

            "breve"

        ]


        if any(
            termo in texto
            for termo in short_terms
        ):

            return "short"


        # =================================================
        # RESPOSTA LONGA
        # =================================================

        long_terms = [

            "explique detalhadamente",
            "explique em detalhes",

            "explica detalhadamente",
            "explica em detalhes",

            "quero uma análise completa",
            "quero uma analise completa",

            "análise completa",
            "analise completa",

            "explique profundamente",
            "explica profundamente",

            "quero entender profundamente",

            "passo a passo completo",

            "guia completo",

            "detalhe tudo",

            "detalhe completamente"

        ]


        if any(
            termo in texto
            for termo in long_terms
        ):

            return "long"


        # =================================================
        # RESPOSTA MÉDIA
        # =================================================

        medium_terms = [

            "como funciona",

            "como fazer",

            "como faço",

            "como criar",

            "por que",

            "porque",

            "qual a diferença",

            "qual é a diferença",

            "qual e a diferença",

            "me explique",

            "me explica",

            "explique",

            "explica",

            "exemplo",

            "exemplos",

            "compare",

            "comparar"

        ]


        if any(
            termo in texto
            for termo in medium_terms
        ):

            return "medium"


        # =================================================
        # PERGUNTAS SIMPLES
        # =================================================

        simple_patterns = [

            r"^o que é .+\?$",
            r"^o que e .+\?$",

            r"^quem é .+\?$",
            r"^quem e .+\?$",

            r"^qual é .+\?$",
            r"^qual e .+\?$",

            r"^quanto é .+\?$",
            r"^quanto e .+\?$"

        ]


        for pattern in simple_patterns:

            if re.match(
                pattern,
                texto
            ):

                return "short"


        # =================================================
        # PADRÃO
        # =================================================

        return "medium"


    # =====================================================
    # CONSTRUIR POLÍTICA
    # =====================================================

    def _build_policy(
        self,
        mensagem,
        resultado
    ):

        user_requested_research = (
            self._user_requested_research(
                mensagem
            )
        )


        automatic_research = (
            self._needs_automatic_research(
                mensagem,
                resultado
            )
        )


        needs_research = (

            user_requested_research

            or

            automatic_research

        )


        response_length = (
            self._response_length(
                mensagem
            )
        )


        # =================================================
        # PROFUNDIDADE
        # =================================================

        if not needs_research:

            research_depth = "none"

        elif response_length == "long":

            research_depth = "deep"

        else:

            research_depth = "normal"


        # =================================================
        # MOTIVO
        # =================================================

        if user_requested_research:

            research_reason = (
                "user_requested"
            )

        elif automatic_research:

            research_reason = (
                "automatic_current_information"
            )

        else:

            research_reason = (
                "none"
            )


        return {

            "needs_research":
                needs_research,

            "user_requested_research":
                user_requested_research,

            "automatic_research":
                automatic_research,

            "research_reason":
                research_reason,

            "response_length":
                response_length,

            "research_depth":
                research_depth

        }


    # =====================================================
    # PROCESSAR
    # =====================================================

    def process(
        self,
        usuario,
        mensagem
    ):

        # ================================================
        # PROTEÇÃO
        # ================================================

        if not mensagem:

            mensagem = ""


        # ================================================
        # DETECTORES
        # ================================================

        resultado = detector_manager.detect(

            mensagem

        )


        if not resultado:

            resultado = {

                "intent":
                    "chat"

            }


        intent = resultado.get(

            "intent",

            "chat"

        )


        # ================================================
        # POLÍTICA
        # ================================================

        policy = self._build_policy(

            mensagem,

            resultado

        )


        # ================================================
        # LOG
        # ================================================

        print(
            "=============================================="
        )

        print(
            "L.I.Z.A RESPONSE POLICY"
        )

        print(
            "Intent:",
            intent
        )

        print(
            "Needs research:",
            policy[
                "needs_research"
            ]
        )

        print(
            "User requested research:",
            policy[
                "user_requested_research"
            ]
        )

        print(
            "Automatic research:",
            policy[
                "automatic_research"
            ]
        )

        print(
            "Research reason:",
            policy[
                "research_reason"
            ]
        )

        print(
            "Research depth:",
            policy[
                "research_depth"
            ]
        )

        print(
            "Response length:",
            policy[
                "response_length"
            ]
        )

        print(
            "=============================================="
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
        # PESQUISA WEB
        # ================================================

        if policy[
            "needs_research"
        ]:

            query = resultado.get(

                "query",

                mensagem

            )


            # ============================================
            # REMOVER COMANDO DA QUERY
            #
            # "Liza, pesquise sobre Kotlin"
            #
            # vira:
            #
            # "Kotlin"
            # ============================================

            query = self._clean_research_query(

                mensagem,

                query

            )


            try:

                pesquisa = (

                    self.research_service.research(

                        query,

                        response_length=
                            policy[
                                "response_length"
                            ]

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

                        ),

                    "responseLength":
                        pesquisa.get(

                            "responseLength",

                            policy[
                                "response_length"
                            ]

                        ),

                    "researchDepth":
                        pesquisa.get(

                            "researchDepth",

                            policy[
                                "research_depth"
                            ]

                        ),

                    "researchReason":
                        policy[
                            "research_reason"
                        ],

                    "userRequestedResearch":
                        policy[
                            "user_requested_research"
                        ]

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
        # PROGRAMADOR
        # ================================================

        if intent == "programmer":

            return agent_manager.execute(

                "programmer",

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


    # =====================================================
    # LIMPAR QUERY DE PESQUISA
    # =====================================================

    def _clean_research_query(
        self,
        mensagem,
        query
    ):

        texto = (
            query
            .strip()
        )


        if not texto:

            return mensagem.strip()


        # ================================================
        # PREFIXOS
        # ================================================

        prefixes = [

            r"^liza[,\s]+",

            r"^liza\s*[:\-]\s*"

        ]


        for pattern in prefixes:

            texto = re.sub(

                pattern,

                "",

                texto,

                flags=re.IGNORECASE

            )


        # ================================================
        # COMANDOS DE PESQUISA
        # ================================================

        commands = [

            r"^faça uma pesquisa\s+(?:sobre\s+)?",
            r"^faca uma pesquisa\s+(?:sobre\s+)?",

            r"^fazer uma pesquisa\s+(?:sobre\s+)?",

            r"^faça uma busca\s+(?:sobre\s+)?",
            r"^faca uma busca\s+(?:sobre\s+)?",

            r"^fazer uma busca\s+(?:sobre\s+)?",

            r"^pesquise\s+(?:sobre\s+)?",
            r"^pesquisa\s+(?:sobre\s+)?",
            r"^pesquisar\s+(?:sobre\s+)?",

            r"^procure\s+(?:sobre\s+)?",
            r"^procura\s+(?:sobre\s+)?",

            r"^busque\s+(?:sobre\s+)?",
            r"^busca\s+(?:sobre\s+)?"

        ]


        for pattern in commands:

            texto = re.sub(

                pattern,

                "",

                texto,

                flags=re.IGNORECASE

            )


        # ================================================
        # CONECTORES DESNECESSÁRIOS
        # ================================================

        texto = re.sub(

            r"^(na internet|na web)\s+",

            "",

            texto,

            flags=re.IGNORECASE

        )


        # ================================================
        # LIMPEZA FINAL
        # ================================================

        texto = texto.strip()


        if not texto:

            return mensagem.strip()


        return texto


# ========================================================
# INSTÂNCIA GLOBAL
# ========================================================

decision_engine = DecisionEngine()