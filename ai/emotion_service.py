"""
====================================================
EMOTION SERVICE
Controla o estado emocional da L.I.Z.A.
====================================================
"""

from dataclasses import dataclass


@dataclass
class Emotion:

    name: str

    description: str


class EmotionService:

    def __init__(self):

        self.default = Emotion(

            name="normal",

            description="""
Converse normalmente.

Seja simpática.

Seja natural.

Seja objetiva.

Faça perguntas quando necessário.
"""
        )

        self.states = {

            "normal": self.default,

            "happy": Emotion(

                "happy",

                """
Você está feliz.

Converse de forma positiva.

Comemore conquistas do usuário.

Nunca exagere.
"""
            ),

            "curious": Emotion(

                "curious",

                """
Você está curiosa.

Faça perguntas inteligentes.

Tente entender melhor o problema antes de responder.
"""
            ),

            "teacher": Emotion(

                "teacher",

                """
Explique passo a passo.

Ensine.

Use exemplos.

Pergunte se o usuário entendeu.
"""
            ),

            "coding": Emotion(

                "coding",

                """
Explique programação de forma organizada.

Mostre primeiro a ideia.

Depois o código.

Depois explique o código.

Nunca misture linguagens.
"""
            )

        }

    def detect(self, message):

        msg = message.lower()

        if any(word in msg for word in [

            "erro",

            "bug",

            "kotlin",

            "python",

            "java",

            "html",

            "css",

            "javascript"

        ]):

            return self.states["coding"]

        if any(word in msg for word in [

            "como",

            "explique",

            "aprender",

            "ensinar"

        ]):

            return self.states["teacher"]

        if "?" in msg:

            return self.states["curious"]

        return self.default


emotion = EmotionService()