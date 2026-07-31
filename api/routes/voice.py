"""
====================================================
VOICE ROUTE
====================================================
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import send_file

import asyncio
import edge_tts
import os

voice_bp = Blueprint(
    "voice",
    __name__
)

VOICE = "pt-BR-FranciscaNeural"

AUDIO_FILE = "liza.mp3"


async def gerar_audio(texto):

    communicate = edge_tts.Communicate(
        text=texto,
        voice=VOICE
    )

    await communicate.save(AUDIO_FILE)


@voice_bp.route("/tts", methods=["POST"])
def tts():

    dados = request.json or {}

    texto = dados.get("text", "").strip()

    if not texto:

        return jsonify({

            "success": False,

            "error": "Texto vazio."

        }), 400

    try:

        asyncio.run(
            gerar_audio(texto)
        )

        return send_file(
            AUDIO_FILE,
            mimetype="audio/mpeg",
            as_attachment=False
        )

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500