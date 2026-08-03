"""
====================================================
L.I.Z.A Command Detector
====================================================
"""

from commands.command_matcher import matcher


class CommandDetector:

    def detect(self, message):

        texto = message.lower().strip()

        # ====================================================
        # COMANDOS FIXOS (Banco de comandos)
        # ====================================================

        resultado = matcher.detect(message)

        if resultado is not None:

            return resultado

        # ====================================================
        # PESQUISA NO YOUTUBE
        # ====================================================

        if "youtube" in texto:

            if "pesquise" in texto or "procure" in texto:

                query = texto

                for palavra in [

                    "pesquise",
                    "procure",
                    "youtube",
                    "no youtube",
                    "por",

                ]:

                    query = query.replace(palavra, "")

                query = query.strip()

                return {

                    "intent": "android",

                    "action": "YOUTUBE_SEARCH",

                    "parameters": {

                        "query": query

                    }

                }

        # ====================================================
        # PESQUISA GOOGLE
        # ====================================================

        if "google" in texto:

            if "pesquise" in texto or "procure" in texto:

                query = texto

                for palavra in [

                    "pesquise",
                    "procure",
                    "google",
                    "no google",
                    "por"

                ]:

                    query = query.replace(palavra, "")

                query = query.strip()

                return {

                    "intent": "android",

                    "action": "GOOGLE_SEARCH",

                    "parameters": {

                        "query": query

                    }

                }

        # ====================================================
        # PLAYLIST SPOTIFY
        # ====================================================

        if "playlist" in texto and "spotify" in texto:

            playlist = texto

            for palavra in [

                "toque",
                "abrir",
                "abra",
                "spotify",
                "playlist"

            ]:

                playlist = playlist.replace(

                    palavra,

                    ""

                )

            playlist = playlist.strip()

            return {

                "intent": "android",

                "action": "PLAY_PLAYLIST",

                "parameters": {

                    "playlist": playlist

                }

            }

        # ====================================================
        # LIGAÇÃO
        # ====================================================

        if texto.startswith("ligue para"):

            contato = texto.replace(

                "ligue para",

                ""

            ).strip()

            return {

                "intent": "android",

                "action": "CALL",

                "parameters": {

                    "contact": contato

                }

            }

        # ====================================================
        # WHATSAPP
        # ====================================================

        if texto.startswith("envie mensagem para"):

            restante = texto.replace(

                "envie mensagem para",

                ""

            ).strip()

            contato = restante

            mensagem = ""

            if " dizendo " in restante:

                contato, mensagem = restante.split(

                    " dizendo ",

                    1

                )

            return {

                "intent": "android",

                "action": "SEND_WHATSAPP",

                "parameters": {

                    "contact": contato.strip(),

                    "message": mensagem.strip()

                }

            }

        # ====================================================
        # EMAIL
        # ====================================================

        if texto.startswith("envie email para"):

            restante = texto.replace(

                "envie email para",

                ""

            ).strip()

            destinatario = restante

            mensagem = ""

            if " dizendo " in restante:

                destinatario, mensagem = restante.split(

                    " dizendo ",

                    1

                )

            return {

                "intent": "android",

                "action": "SEND_EMAIL",

                "parameters": {

                    "to": destinatario.strip(),

                    "message": mensagem.strip()

                }

            }

        # ====================================================
        # SEM COMANDO
        # ====================================================

        return None