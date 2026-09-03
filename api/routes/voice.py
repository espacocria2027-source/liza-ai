"""
====================================================
VOICE ROUTE
====================================================
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response
from flask import stream_with_context

import asyncio
import edge_tts
import time


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

    inicio = time.perf_counter()

    print("=" * 60)
    print("EDGE-TTS INICIADO")
    print("Texto:", texto)
    print("=" * 60)

    communicate = edge_tts.Communicate(
        text=texto,
        voice=VOICE
    )

    primeiro_audio = True
    total_bytes = 0
    total_chunks = 0

    async for chunk in communicate.stream():

        if chunk["type"] != "audio":
            continue

        audio = chunk["data"]

        if not audio:
            continue

        total_chunks += 1
        total_bytes += len(audio)

        # --------------------------------------------
        # PRIMEIRO ÁUDIO
        # --------------------------------------------

        if primeiro_audio:

            primeiro_audio = False

            tempo_primeiro_audio = (
                time.perf_counter() - inicio
            )

            print(
                f"🎵 PRIMEIRO ÁUDIO: "
                f"{tempo_primeiro_audio:.3f}s"
            )

        yield audio

    tempo_total = (
        time.perf_counter() - inicio
    )

    print("=" * 60)
    print("EDGE-TTS FINALIZADO")
    print(
        f"Chunks: {total_chunks}"
    )
    print(
        f"Bytes: {total_bytes}"
    )
    print(
        f"Tempo total: {tempo_total:.3f}s"
    )
    print("=" * 60)


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

                if chunk:
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

        try:

            loop.close()

        except Exception:

            pass


# ====================================================
# TTS
# ====================================================

@voice_bp.route(
    "/tts",
    methods=["POST"]
)
def tts():

    dados = request.get_json(
        silent=True
    ) or {}

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

        response = Response(

            stream_with_context(
                gerar_stream(texto)
            ),

            mimetype="audio/mpeg",

            headers={

                "Cache-Control":
                    "no-cache, no-store, must-revalidate",

                "Pragma":
                    "no-cache",

                "Expires":
                    "0",

                "Connection":
                    "keep-alive",

                "X-Accel-Buffering":
                    "no"

            }

        )

        return response


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500