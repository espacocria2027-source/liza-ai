"""
====================================================
Research Detector
====================================================
"""

import re


class ResearchDetector:

    # ==================================================
    # PALAVRAS QUE INDICAM PESQUISA ATUAL
    # ==================================================

    CURRENT_KEYWORDS = (

        "atual",

        "atualmente",

        "hoje",

        "agora",

        "recentemente",

        "recente",

        "último",

        "última",

        "últimos",

        "últimas",

        "mais recente",

        "mais recentes",

        "versão atual",

        "versão mais recente",

        "notícias",

        "notícia",

        "aconteceu hoje",

        "acontecendo",

        "lançamento",

        "lançada",

        "lançado",

        "preço atual",

        "valor atual",

        "cotação",

        "clima",

        "tempo agora"

    )


    # ==================================================
    # EXPRESSÕES QUE NORMALMENTE PRECISAM DA WEB
    # ==================================================

    RESEARCH_PATTERNS = (

        r"\bqual\s+(é|e)\s+a\s+versão",

        r"\bqual\s+(é|e)\s+o\s+preço",

        r"\bquanto\s+custa",

        r"\bquanto\s+está",

        r"\bquem\s+é\s+o\s+atual",

        r"\bquem\s+é\s+a\s+atual",

        r"\bo\s+que\s+aconteceu",

        r"\bo\s+que\s+está\s+acontecendo",

        r"\bqual\s+é\s+a\s+situação",

        r"\bcomo\s+está\s+",

        r"\bpesquise\s+",

        r"\bpesquisa\s+",

        r"\bprocure\s+",

        r"\bconsulte\s+",

        r"\bverifique\s+",

        r"\bconfira\s+"

    )


    # ==================================================
    # DETECTAR
    # ==================================================

    def detect(
        self,
        message
    ):

        if not message:

            return None


        text = (
            str(message)
            .strip()
            .lower()
        )


        if not text:

            return None


        # ==================================================
        # PESQUISA EXPLÍCITA
        # ==================================================

        if self._has_explicit_research(
            text
        ):

            return {

                "intent":
                    "research",

                "query":
                    message

            }


        # ==================================================
        # INFORMAÇÃO ATUAL
        # ==================================================

        if self._has_current_information(
            text
        ):

            return {

                "intent":
                    "research",

                "query":
                    message

            }


        return None


    # ==================================================
    # PESQUISA EXPLÍCITA
    # ==================================================

    def _has_explicit_research(
        self,
        text
    ):

        explicit_words = (

            "pesquise",

            "pesquisa",

            "procure",

            "buscar na internet",

            "busque na internet",

            "pesquisar na internet",

            "na web",

            "na internet",

            "fontes",

            "fontes confiáveis",

            "verifique na web",

            "consulte a internet"

        )


        return any(

            word in text

            for word in explicit_words

        )


    # ==================================================
    # INFORMAÇÃO ATUAL
    # ==================================================

    def _has_current_information(
        self,
        text
    ):

        # ----------------------------------------------
        # PALAVRAS-CHAVE
        # ----------------------------------------------

        if any(

            keyword in text

            for keyword
            in self.CURRENT_KEYWORDS

        ):

            return True


        # ----------------------------------------------
        # PADRÕES
        # ----------------------------------------------

        for pattern in self.RESEARCH_PATTERNS:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            ):

                return True


        return False