"""
====================================================
Programmer Detector
====================================================
"""


class ProgrammerDetector:

    def detect(self, message):

        if not message:

            return None


        texto = (
            message
            .lower()
            .strip()
        )


        if not texto:

            return None


        # ==================================================
        # PERGUNTAS QUE PRECISAM DE PESQUISA
        # ==================================================

        research_indicators = [

            "atual",

            "atualmente",

            "hoje",

            "agora",

            "recente",

            "recentemente",

            "mais recente",

            "mais recentes",

            "último",

            "última",

            "últimos",

            "últimas",

            "versão atual",

            "versão mais recente",

            "preço atual",

            "valor atual",

            "lançamento",

            "lançada",

            "lançado",

            "notícia",

            "notícias",

            "pesquise",

            "pesquisa",

            "procure",

            "busque",

            "buscar",

            "internet",

            "web"

        ]


        # ==================================================
        # SE A PERGUNTA EXIGE INFORMAÇÃO ATUAL,
        # NÃO DEIXAMOS O PROGRAMMER DETECTOR CAPTURAR.
        # ==================================================

        for indicador in research_indicators:

            if indicador in texto:

                return None


        # ==================================================
        # TERMOS DE PROGRAMAÇÃO
        # ==================================================

        palavras = [

            "python",

            "java",

            "kotlin",

            "flutter",

            "javascript",

            "typescript",

            "html",

            "css",

            "api",

            "firebase",

            "sql",

            "programação",

            "programacao",

            "código",

            "codigo"

        ]


        # ==================================================
        # DETECÇÃO
        # ==================================================

        for palavra in palavras:

            if palavra in texto:

                return {

                    "intent":
                        "programmer"

                }


        return None