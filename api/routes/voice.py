"""
====================================================
VOICE ROUTE
====================================================
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response

import asyncio
import edge_tts
import json


# ====================================================
# BLUEPRINT
# ====================================================

voice_bp = Blueprint(
    "voice",
    __name__
)


# ====================================================
# CONFIGURAÇÃO
# ====================================================

VOICE = "pt-BR-FranciscaNeural"


# ====================================================
# GERAR STREAM DE ÁUDIO
# ====================================================

async def gerar_audio(texto):

    communicate = edge_tts.Communicate(
        text=texto,
        voice=VOICE
    )

    async for chunk in communicate.stream():

        # --------------------------------------------
        # SOMENTE DADOS DE ÁUDIO
        # --------------------------------------------

        if chunk["type"] == "audio":

            audio = chunk["data"]

            if audio:

                yield audio


# ====================================================
# GERADOR SÍNCRONO PARA FLASK
# ====================================================

def gerar_stream(texto):

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    generator = gerar_audio(texto)

    try:

        while True:

            try:

                chunk = loop.run_until_complete(
                    generator.__anext__()
                )

                yield chunk

            except StopAsyncIteration:

                break

    finally:

        try:

            loop.run_until_complete(
                generator.aclose()
            )

        except Exception:

            pass

        loop.close()


# ====================================================
# TTS
# ====================================================

@voice_bp.route(
    "/tts",
    methods=["POST"]
)
def tts():

    dados = request.json or {}

    texto = (
        dados
        .get("text", "")
        .strip()
    )


    # =================================================
    # TEXTO VAZIO
    # =================================================

    if not texto:

        return jsonify({

            "success": False,

            "error": "Texto vazio."

        }), 400


    try:

        # =============================================
        # STREAMING
        # =============================================

        return Response(

            gerar_stream(texto),

            mimetype="audio/mpeg",

            headers={

                "Cache-Control":
                    "no-cache",

                "Connection":
                    "keep-alive",

                "X-Accel-Buffering":
                    "no"

            }

        )


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500