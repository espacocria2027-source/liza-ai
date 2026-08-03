"""
====================================================
Programmer Detector
====================================================
"""


class ProgrammerDetector:

    def detect(self, message):

        texto = message.lower()

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

        for palavra in palavras:

            if palavra in texto:

                return {

                    "intent": "programmer"

                }

        return None