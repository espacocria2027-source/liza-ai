"""
==================================================
AI INTENT DETECTOR
==================================================
"""

import json
import requests

from config import MODEL_CHAT


OLLAMA = "http://localhost:11434/api/chat"


class AIIntentDetector:

    SYSTEM_PROMPT = """
Você é um classificador de intenções.

Sua única função é retornar JSON.

Nunca explique.

Nunca converse.

Nunca utilize markdown.

Nunca utilize ```.

Responda apenas JSON válido.

Ações disponíveis:

chat

open_app

google_search

youtube_search

open_video

call

send_sms

send_whatsapp

send_email

create_event

create_alarm

create_reminder

open_maps

open_camera

take_photo

open_gallery

flashlight_on

flashlight_off

open_settings

play_spotify

open_browser

share_text

copy_text

Caso não exista ação:

chat

Formato:

{
    "action":"...",
    "data":{

    }
}
"""

    def detect(self, message):

        body = {

            "model": MODEL_CHAT,

            "messages":[

                {

                    "role":"system",

                    "content":self.SYSTEM_PROMPT

                },

                {

                    "role":"user",

                    "content":message

                }

            ],

            "stream":False

        }

        response = requests.post(

            OLLAMA,

            json=body,

            timeout=60

        )

        content = response.json()["message"]["content"]

        content = content.strip()

        try:

            return json.loads(content)

        except Exception:

            return {

                "action":"chat",

                "data":{}

            }


ai_detector = AIIntentDetector()