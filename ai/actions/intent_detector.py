"""
=========================================
L.I.Z.A. INTENT DETECTOR
=========================================
"""

import re

from ai.actions.actions import Action
from ai.actions.app_registry import registry


class IntentDetector:

    def detect(self, message: str):

        text = message.lower().strip()

        # -----------------------------
        # Abrir aplicativos
        # -----------------------------

        app = registry.find(text)

        if app and any(
            word in text for word in [
                "abrir",
                "abra",
                "abrir o",
                "abrir a",
                "inicie",
                "iniciar",
                "executar"
            ]
        ):

            return {
                "action": Action.OPEN_APP,
                "data": {
                    "package": app.package,
                    "app_name": app.name
                }
            }

        # -----------------------------
        # Google
        # -----------------------------

        google = re.search(

            r"(pesquise|procure|buscar|busque)(.*)(google)",

            text

        )

        if google:

            query = google.group(2).strip()

            return {

                "action": Action.GOOGLE_SEARCH,

                "data": {

                    "query": query

                }

            }

        # -----------------------------
        # YouTube
        # -----------------------------

        youtube = re.search(

            r"(pesquise|procure|buscar|busque)(.*)(youtube)",

            text

        )

        if youtube:

            query = youtube.group(2).strip()

            return {

                "action": Action.YOUTUBE_SEARCH,

                "data": {

                    "query": query

                }

            }

        # -----------------------------
        # Ligação
        # -----------------------------

        call = re.search(

            r"(ligue para|ligar para|telefone para)(.*)",

            text

        )

        if call:

            return {

                "action": Action.CALL,

                "data": {

                    "contact": call.group(2).strip()

                }

            }

        # -----------------------------
        # WhatsApp
        # -----------------------------

        zap = re.search(

            r"(mande mensagem para|envie mensagem para)(.*)",

            text

        )

        if zap:

            return {

                "action": Action.SEND_WHATSAPP,

                "data": {

                    "contact": zap.group(2).strip(),

                    "message": ""

                }

            }

        # -----------------------------
        # Gmail
        # -----------------------------

        if "email" in text or "gmail" in text:

            return {

                "action": Action.SEND_EMAIL,

                "data": {}

            }

        # -----------------------------
        # Agenda
        # -----------------------------

        if "agenda" in text:

            return {

                "action": Action.CREATE_EVENT,

                "data": {}

            }

        # -----------------------------
        # Câmera
        # -----------------------------

        if "tirar foto" in text:

            return {

                "action": Action.TAKE_PHOTO,

                "data": {}

            }

        if "abrir câmera" in text or "abra a câmera" in text:

            return {

                "action": Action.OPEN_CAMERA,

                "data": {}

            }

        # -----------------------------
        # Lanterna
        # -----------------------------

        if "ligar lanterna" in text:

            return {

                "action": Action.FLASHLIGHT_ON,

                "data": {}

            }

        if "desligar lanterna" in text:

            return {

                "action": Action.FLASHLIGHT_OFF,

                "data": {}

            }

        # -----------------------------
        # Configurações
        # -----------------------------

        if "configurações" in text or "configuracoes" in text:

            return {

                "action": Action.OPEN_SETTINGS,

                "data": {}

            }

        # -----------------------------
        # Conversa
        # -----------------------------

        return {

            "action": Action.CHAT,

            "data": {}

        }


intent_detector = IntentDetector()